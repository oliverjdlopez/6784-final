import torch
import torch.nn as nn
from ray.rllib.models.tf.misc import normc_initializer
from ray.rllib.models.torch.misc import SlimFC
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
import numpy as np
from ray.rllib.utils import override

class LinearNN(TorchModelV2, nn.Module):
    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        TorchModelV2.__init__(
            self, obs_space, action_space, num_outputs, model_config, name
        )
        nn.Module.__init__(self)
        print(f"num_outputs: {num_outputs} . obs_space shape: {obs_space.shape}. model config: {model_config}")
        # hidden_dim = model_config["custom_model_config"]["hidden_dim"]

        hidden_dim = 128
        hidden_dim2 = 59
        # self.embedding = nn.Linear(obs_space.shape[0], hidden_dim2)
        # self.fc1 = nn.Linear(hidden_dim2, hidden_dim)
        self.fc1 = nn.Linear(obs_space.shape[0], hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.relu = nn.ReLU()
        # self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, num_outputs)
        self._last_batch_size = None
        self._features = None

        m100_dict = torch.load("/Users/ahmedmoustafa/School/FA23/CS6784/6784-final/simulator/models/nn/m100_dict2", map_location=torch.device('cpu'))

        print(f"stats: {m100_dict['fc1.weight'].shape}, {m100_dict['fc1.bias'].shape}, {m100_dict['fc2.weight'].shape}, {m100_dict['fc2.bias'].shape}")
        # self.fc1.weight = torch.nn.Parameter(m100_dict["fc1.weight"])
        # self.fc1.bias = torch.nn.Parameter(m100_dict["fc1.bias"])
        #
        # self.fc2.weight = torch.nn.Parameter(m100_dict["fc2.weight"])
        # self.fc2.bias = torch.nn.Parameter(m100_dict["fc2.bias"])

        self.eval()

        self._value_branch = SlimFC(
            in_size=hidden_dim // 2,
            out_size=1,
            activation_fn=None,
        )

    @override(TorchModelV2)
    def forward(self, input_dict, state, seq_lens):
        x = input_dict["obs_flat"].float()
        if torch.isnan(x).any():
            print(f"NaN input: {x}")
        # x = self.embedding(x)
        x = self.relu(self.bn1(self.fc1(x)))
        # x = self.dropout(x)
        self._features = self.relu(self.bn2(self.fc2(x)))
        x = torch.softmax(self.fc3(self._features), dim=1)
        return x, state

    @override(TorchModelV2)
    def value_function(self):
        assert self._features is not None, "must call forward() first"
        y = self._value_branch(self._features).squeeze(1)
        return y
