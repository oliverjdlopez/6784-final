import torch
import torch.nn as nn
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
import numpy as np
from ray.rllib.utils import override
from torch import TensorType


class LinearNN(TorchModelV2, nn.Module):
    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        TorchModelV2.__init__(
            self, obs_space, action_space, num_outputs, model_config, name
        )
        nn.Module.__init__(self)
        print(f"num_outputs: {num_outputs} . obs_space shape: {obs_space.shape}. model config: {model_config}")
        # hidden_dim = model_config["custom_model_config"]["hidden_dim"]
        hidden_dim = 128
        self.fc1 = nn.Linear(obs_space.shape[0], hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, num_outputs)
        self._last_batch_size = None

    @override(TorchModelV2)
    def forward(self, input_dict, state, seq_lens):
        self._last_batch_size = input_dict["obs"].shape[0]
        x = input_dict["obs_flat"].float()
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.fc3(x)
        return x, state

    # @override(TorchModelV2)
    # def value_function(self) -> TensorType:
    #     assert self._features is not None, "must call forward() first"
    #     if self._value_branch_separate:
    #         out = self._value_branch(
    #             self._value_branch_separate(self._last_flat_in)
    #         ).squeeze(1)
    #     else:
    #         out = self._value_branch(self._features).squeeze(1)
    #     return out

    def value_function(self):
        return torch.from_numpy(np.zeros(shape=(self._last_batch_size,)))
