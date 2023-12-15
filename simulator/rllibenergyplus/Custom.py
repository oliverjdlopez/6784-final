import torch
from ray.rllib.policy.policy import Policy
from ray.rllib.core.rl_module import RLModule
from ray.rllib.core.rl_module.rl_module import RLModuleConfig
#left off:
    # Option 1: try to just plug this into PPO and see how it works on env
    # option 2: use step function to run as simulator

class CustomModule(RLModule):
    def __init__(self, config: RLModuleConfig):
        super().__init__(config)

    #for reasons due to ray architecture, do normal initialization work in suetup
    def setup(self):
        self.input_dim = self.config.observation_space.shape[0]
        self.policy = None

    def _forward_inference(self,batch):
        with torch.no_grad():
            return self._forward_train(batch)

    def _forward_exploration(self, batch):
        with torch.no_grad():
            return self._forward_train(batch)

    def _forward_train(self,batch):
        out = {"actions": self.action_space.sample() for _ in batch}
        return self.policy(batch)

    def get_state(self):
        pass

    def set_state(self):
        pass


def simulate_with_pretrained(checkpoint_path, env):
    model = torch.load(checkpoint_path)
    n_steps = 10
    for _ in range(n_steps):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        if done:
            break
    print("done")