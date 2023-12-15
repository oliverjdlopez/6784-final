import argparse
import os
import threading
from queue import Queue, Empty, Full
from tempfile import TemporaryDirectory
from typing import Dict, Any, Tuple, Optional, List
import torch
import torch.nn as nn

import gymnasium as gym
import numpy as np
import ray
from gymnasium.spaces import Discrete, MultiDiscrete
from ray import tune, air
from ray.rllib.algorithms.ppo import PPOConfig

from pyenergyplus.api import EnergyPlusAPI
from pyenergyplus.datatransfer import DataExchange


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--idf",
        help="Path to .idf file",
        required=True
    )
    parser.add_argument(
        "--epw",
        help="Path to weather file",
        required=True
    )
    parser.add_argument(
        "--csv",
        help="Generate eplusout.csv at end of simulation",
        required=False,
        default=False,
        action="store_true"
    )
    parser.add_argument(
        "--output",
        help="EnergyPlus output directory. Default is a generated one in /tmp/",
        required=False,
        default=TemporaryDirectory().name
    )
    parser.add_argument(
        "--timesteps", "-t",
        help="Number of timesteps to train",
        required=False,
        default=1e6
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=2,
        help="The number of workers to use",
    )
    parser.add_argument(
        "--num-gpus",
        type=int,
        default=0,
        help="The number of GPUs to use",
    )
    parser.add_argument(
        "--alg",
        default="PPO",
        choices=["APEX", "DQN", "IMPALA", "PPO", "R2D2"],
        help="The algorithm to use",
    )
    parser.add_argument(
        "--framework",
        choices=["tf", "tf2", "tfe", "torch"],
        default="tf",
        help="The deep learning framework specifier",
    )
    parser.add_argument(
        "--use-lstm",
        action="store_true",
        help="Whether to auto-wrap the model with an LSTM. Only valid option for "
             "--run=[IMPALA|PPO|R2D2]",
    )
    built_args = parser.parse_args()
    print(f"Running with following CLI args: {built_args}")
    return built_args


class EnergyPlusRunner:

    def __init__(self, episode: int, env_config: Dict[str, Any], obs_queue: Queue, act_queue: Queue) -> None:
        self.episode = episode
        self.env_config = env_config
        self.obs_queue = obs_queue
        self.act_queue = act_queue

        self.energyplus_api = EnergyPlusAPI()
        self.x: DataExchange = self.energyplus_api.exchange
        self.energyplus_exec_thread: Optional[threading.Thread] = None
        self.energyplus_state: Any = None
        self.sim_results: Dict[str, Any] = {}
        self.initialized = False
        self.progress_value: int = 0
        self.simulation_complete = False

        # below is declaration of variables, meters and actuators
        # this simulation will interact with
        self.variables = {
            # °C
            "oat": ("Site Outdoor Air DryBulb Temperature", "Environment"),
            # °C
            "w_iat": ("Zone Mean Air Temperature", "WEST ZONE"),
            # °C
            "e_iat": ("Zone Mean Air Temperature", "EAST ZONE"),
            # °C
            "w_rat": ("System Node Temperature", "WEST ZONE INLET NODE"),
            # °C
            "e_rat": ("System Node Temperature", "WEST ZONE INLET NODE"),
            # rh%
            "w_rh": ("Zone Air Relative Humidity", "WEST ZONE"),
            # rh%
            "e_rh": ("Zone Air Relative Humidity", "EAST ZONE"),
            # °C
            "w_hvac_tspt": ("System Node Setpoint Temperature", "WEST AIR LOOP OUTLET NODE"),
            # °C
            "e_hvac_tspt": ("System Node Setpoint Temperature", "EAST AIR LOOP OUTLET NODE")
        }
        self.var_handles: Dict[str, int] = {}

        self.meters = {
            "cooling_elec": "Cooling:Electricity",
            "plant_elec": "Electricity:Plant",
            # HVAC electricity usage (J)
            "hvac_elec": "Electricity:HVAC",
            "building_elec": "Electricity:Building",
            "it_elec": "ITE-CPU:InteriorEquipment:Electricity"
        }
        self.meter_handles: Dict[str, int] = {}

        self.actuators = {
            # WEST zone HVAC air loop temperature setpoint (°C)
            "w_sat_spt": (
                "System Node Setpoint",
                "Temperature Setpoint",
                "WEST AIR LOOP OUTLET NODE"
            ),
            # EAST zone HVAC air loop air temperature setpoint (°C)
            "e_sat_spt": (
                "System Node Setpoint",
                "Temperature Setpoint",
                "EAST AIR LOOP OUTLET NODE"
            ),
            # WEST zone HVAC air loop air flow rate setpoint (m3/s)
            "w_hvac_fr": (
                "System Node Setpoint",
                "Mass Flow Rate Setpoint",
                "WEST AIR LOOP OUTLET NODE"
            ),
            # EAST zone HVAC air loop air flow rate setpoint (m3/s)
            "e_hvac_fr": (
                "System Node Setpoint",
                "Mass Flow Rate Setpoint",
                "EAST AIR LOOP OUTLET NODE"
            )
        }
        self.actuator_handles: Dict[str, int] = {}

    def start(self) -> None:
        self.energyplus_state = self.energyplus_api.state_manager.new_state()
        runtime = self.energyplus_api.runtime

        # register callback used to track simulation progress
        def _report_progress(progress: int) -> None:
            self.progress_value = progress
            print(f"Simulation progress: {self.progress_value}%")

        runtime.callback_progress(self.energyplus_state, _report_progress)

        # register callback used to collect observations
        runtime.callback_end_zone_timestep_after_zone_reporting(self.energyplus_state, self._collect_obs)

        # register callback used to send actions
        runtime.callback_after_predictor_after_hvac_managers(self.energyplus_state, self._send_actions)

        # run EnergyPlus in a non-blocking way
        def _run_energyplus(runtime, cmd_args, state, results):
            print(f"running EnergyPlus with args: {cmd_args}")

            # start simulation
            results["exit_code"] = runtime.run_energyplus(state, cmd_args)

            if not self.simulation_complete:
                # free consumers from waiting
                self.obs_queue.put(None)
                self.act_queue.put(None)
                self.stop()

        self.energyplus_exec_thread = threading.Thread(
            target=_run_energyplus,
            args=(
                self.energyplus_api.runtime,
                self.make_eplus_args(),
                self.energyplus_state,
                self.sim_results
            )
        )
        self.energyplus_exec_thread.start()

    def stop(self) -> None:
        if not self.simulation_complete:
            self.simulation_complete = True
            self._flush_queues()
            self.energyplus_exec_thread.join()
            self.energyplus_exec_thread = None
            self.energyplus_api.runtime.clear_callbacks()
            self.energyplus_api.state_manager.delete_state(self.energyplus_state)

    def failed(self) -> bool:
        return self.sim_results.get("exit_code", -1) > 0

    def make_eplus_args(self) -> List[str]:
        """
        make command line arguments to pass to EnergyPlus
        """
        eplus_args = ["-r"] if self.env_config.get("csv", False) else []
        eplus_args += [
            "-w",
            self.env_config["epw"],
            "-d",
            f"{self.env_config['output']}/episode-{self.episode:08}-{os.getpid():05}",
            self.env_config["idf"]
        ]
        return eplus_args

    def _collect_obs(self, state_argument) -> None:
        """
        EnergyPlus callback that collects output variables/meters
        values and enqueue them
        """
        if self.simulation_complete or not self._init_callback(state_argument):
            return

        self.next_obs = {
            **{
                key: self.x.get_variable_value(state_argument, handle)
                for key, handle
                in self.var_handles.items()
            },
            **{
                key: self.x.get_meter_value(state_argument, handle)
                for key, handle
                in self.meter_handles.items()
            }
        }
        self.obs_queue.put(self.next_obs)

    def _send_actions(self, state_argument):
        """
        EnergyPlus callback that sets actuator value from last decided action
        """
        if self.simulation_complete or not self._init_callback(state_argument):
            return

        if self.act_queue.empty():
            return

        next_action = self.act_queue.get()
        print(f"Next action: {next_action}")
        # assert isinstance(next_action, list)

        # actions_handles = ["w_sat_spt", "e_sat_spt", "w_zone_spt", "e_zone_spt"]
        actions_handles = ["w_sat_spt", "e_sat_spt", "w_hvac_fr", "e_hvac_fr"]

        for handle_idx in range(len(actions_handles)):
            print(f"taking action {self.actuator_handles[actions_handles[handle_idx]]} : {next_action[handle_idx]}")
            self.x.set_actuator_value(
                state=state_argument,
                actuator_handle=self.actuator_handles[actions_handles[handle_idx]],
                actuator_value=next_action[handle_idx]
            )


    def _init_callback(self, state_argument) -> bool:
        """initialize EnergyPlus handles and checks if simulation runtime is ready"""
        self.initialized = self._init_handles(state_argument) \
                           and not self.x.warmup_flag(state_argument)
        return self.initialized

    def _init_handles(self, state_argument):
        """initialize sensors/actuators handles to interact with during simulation"""
        if not self.initialized:
            if not self.x.api_data_fully_ready(state_argument):
                return False

            self.var_handles = {
                key: self.x.get_variable_handle(state_argument, *var)
                for key, var in self.variables.items()
            }

            self.meter_handles = {
                key: self.x.get_meter_handle(state_argument, meter)
                for key, meter in self.meters.items()
            }

            self.actuator_handles = {
                key: self.x.get_actuator_handle(state_argument, *actuator)
                for key, actuator in self.actuators.items()
            }

            for handles in [
                self.var_handles,
                self.meter_handles,
                self.actuator_handles
            ]:
                if any([v == -1 for v in handles.values()]):
                    available_data = self.x.list_available_api_data_csv(state_argument).decode('utf-8')
                    raise RuntimeError(
                        f"got -1 handle, check your var/meter/actuator names:\n"
                        f"> variables: {self.var_handles}\n"
                        f"> meters: {self.meter_handles}\n"
                        f"> actuators: {self.actuator_handles}\n"
                        f"> available E+ API data: {available_data}"
                    )

            self.initialized = True

        return True

    def _flush_queues(self):
        for q in [self.obs_queue, self.act_queue]:
            while not q.empty():
                q.get()


class EnergyPlusEnv(gym.Env):

    def __init__(self, env_config: Dict[str, Any]):
        self.env_config = env_config
        self.episode = -1
        self.timestep = 0

        # observation space:
        # OAT (-40, 40)
        # W IAT, (0, 40)
        # E IAT, (0, 40)
        # W RAT, (0, 40)
        # E RAT, (0, 40)
        # W rh, (0,100)
        # E rh, (0,100)
        # W HVAC TSPT (0, 40)
        # E HVAC TSPT (0, 40)
        # cooling elec, (0, 1e9)
        # plant elec, (0, 1e9)
        # hvac elec (0, 1e9)
        # building elec (0, 1e9)
        # it equipment elec (0, 1e9)
        low_obs = np.array(
            [-40.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        )
        hig_obs = np.array(
            [40.0, 40.0, 40.0, 40.0, 40.0, 100.0, 100.0, 40.0, 40.0, 1e9, 1e9, 1e9, 1e9, 1e9]
        )

        self.observation_space = gym.spaces.Box(
            low=low_obs, high=hig_obs, dtype=np.float32
        )
        self.last_obs = {}

        # action space: (west HVAC air temp, east HVAC air temp, west HVAC flow rate, east HVAC flow rate) (100 possible values each)
        self.action_space: MultiDiscrete = MultiDiscrete([100, 100, 100, 100])

        self.energyplus_runner: Optional[EnergyPlusRunner] = None
        self.obs_queue: Optional[Queue] = None
        self.act_queue: Optional[Queue] = None

    def reset(
        self, *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ):
        self.episode += 1
        self.last_obs = self.observation_space.sample()

        if self.energyplus_runner is not None:
            self.energyplus_runner.stop()

        # observations and actions queues for flow control
        # queues have a default max size of 1
        # as only 1 E+ timestep is processed at a time
        self.obs_queue = Queue(maxsize=1)
        self.act_queue = Queue(maxsize=1)

        self.energyplus_runner = EnergyPlusRunner(
            episode=self.episode,
            env_config=self.env_config,
            obs_queue=self.obs_queue,
            act_queue=self.act_queue
        )
        self.energyplus_runner.start()

        # wait until E+ is ready.
        obs = self.obs_queue.get()
        self.last_obs = obs
        return np.array(list(obs.values())), {}

    def step(self, action):
        self.timestep += 1
        done = False

        # check for simulation errors
        if self.energyplus_runner.failed():
            raise RuntimeError(f"EnergyPlus failed with {self.energyplus_runner.sim_results['exit_code']}")

        # simulation_complete is likely to happen after last env step()
        # is called, hence leading to waiting on queue for a timeout
        if self.energyplus_runner.simulation_complete:
            done = True
            obs = self.last_obs
        else:
            # rescale agent decision to actuator range
            # this is equivalent to clamping to the safety constraints on the actions
            ranges = [(10, 30), (10, 30), (0, 6), (0, 6)]
            values = [self._rescale(
                n=int(action[i]),  # noqa
                range1=(0, self.action_space.nvec[i]),
                range2=(0, 30)
            ) for i in range(len(action))]

            print(f"Rescaled values: {values}")

            # enqueue action (received by EnergyPlus through dedicated callback)
            # then wait to get next observation.
            # timeout is set to 2s to handle end of simulation cases, which happens async
            # and materializes by worker thread waiting on this queue (EnergyPlus callback
            # not consuming yet/anymore)
            # timeout value can be increased if E+ timestep takes longer
            timeout = 2
            try:
                self.act_queue.put(values, timeout=timeout)
                self.last_obs = obs = self.obs_queue.get(timeout=timeout)
            except (Full, Empty):
                done = True
                obs = self.last_obs

        # compute reward
        reward = self._compute_reward(obs)

        obs_vec = np.array(list(obs.values()))
        return obs_vec, reward, done, False, {}

    def close(self):
        if self.energyplus_runner is not None:
            self.energyplus_runner.stop()

    def render(self, mode="human"):
        pass

    @staticmethod
    def _compute_reward(obs: Dict[str, float]) -> float:
        """compute reward scalar"""
        if obs["w_hvac_tspt"] > 0 and obs["e_hvac_tspt"] > 0:
            vals = np.array([[obs["w_iat"], obs["w_hvac_tspt"]], [obs["e_iat"], obs["e_hvac_tspt"]]])
            tmp_rew = np.diff(vals, axis=1).squeeze()

            tmp_rew = tmp_rew[tmp_rew < 0]
            tmp_rew = np.max(np.abs(tmp_rew)) if tmp_rew.size > 0 else 0
        else:
            tmp_rew = 0

        reward = -(1e-8 * (obs["cooling_elec"] + obs["plant_elec"] + obs["hvac_elec"] + obs["building_elec"] + obs["it_elec"])) - tmp_rew
        return reward

    @staticmethod
    def _rescale(
        n: int,
        range1: Tuple[float, float],
        range2: Tuple[float, float]
    ) -> float:
        delta1 = range1[1] - range1[0]
        delta2 = range2[1] - range2[0]
        return (delta2 * (n - range1[0]) / delta1) + range2[0]


if __name__ == "__main__":
    args = parse_args()

    ray.init()

    # Ray configuration. See Ray docs for tuning
    config = (
        PPOConfig()
        .environment(
            env=EnergyPlusEnv,
            env_config=vars(args)
        )
        .training(
            gamma=0.95,
            lr=0.003,
            kl_coeff=0.3,
            train_batch_size=4000,
            sgd_minibatch_size=128,
            vf_loss_coeff=0.01,
            use_critic=True,
            use_gae=True,
            model={
                "use_lstm": args.use_lstm,
                "vf_share_layers": False,
            },
            _enable_learner_api=True,
        )
        .rl_module(_enable_rl_module_api=True)
        .framework(
            framework=args.framework,
            eager_tracing=args.framework == "tf2",
        )
        .resources(num_gpus=args.num_gpus)
        .rollouts(
            num_rollout_workers=args.num_workers,
            rollout_fragment_length="auto",
        )
    )

    print("PPO config:", config.to_dict())

    tune.Tuner(
        "PPO",
        run_config=air.RunConfig(
            stop={"timesteps_total": args.timesteps},
            failure_config=air.FailureConfig(max_failures=0, fail_fast=True),
        ),
        param_space=config.to_dict(),
    ).fit()

    ray.shutdown()