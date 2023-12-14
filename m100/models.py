import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim
from torch.utils.data import DataLoader

class LinearNN(nn.Module):
    def __init__(self, feature_dim, action_dim, hidden_dim=128):
        super(EnhancedLinearNN, self).__init__()
        self.fc1 = nn.Linear(feature_dim + action_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, feature_dim)

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        return self.fc3(x)


def train(model, trainloader, optimizer, loss_fn, epochs, scheduler=None, batches=-1):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()
    for e in range(epochs):
        for ii, (inputs, labels) in enumerate(trainloader):
            if batches != -1 and ii >= batches:
                break
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            if scheduler:
                scheduler.step()
        print(f"Epoch {e+1}/{epochs}, Loss: {loss.item()}")
    model.eval()
class StateEstimator:
    def __init__(self, s0):
        # Truths
        self.dim = s0.shape[0]
        self.I = 1
        self.st = s0

        measurement_noise = self.get_measurement_noise()
        filtered_y = self.H @ self.st
        yt = filtered_y + measurement_noise

        self.filtered_y = filtered_y
        self.yt = yt
        self.prev_s_hat = s0_hat

        self.measurement_history = [yt]
        self.filtered_y_history = [filtered_y]
        self.state_history = [s0_hat]
        self.noise_history = [measurement_noise]
        self.L_history = [self.gain()]


    def get_measurement_noise(self, variance=0.3):
        return np.random.normal(scale=variance)

    def get_system_noise(self, variance=0.3):
        return np.random.normal(scale=variance, size=self.dim)

    # update internal matrix, return new state according to dynamics
    def extrapolate(self):
        extrap_s_hat = self.F @ self.prev_s_hat
        self.P = self.F @ self.P @ self.F + self.I
        return extrap_s_hat

    def gain(self):
        return self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.I)

        # predict new state with kalman filter

    def predict_kalman(self):
        st_hat = self.extrapolate()
        L = self.gain()
        s_hat = st_hat + L @ (self.yt - self.H @ st_hat)
        return s_hat

    # predict new state with kalman filter
    def predict_steady_kalman(self):
        s_hat = self.F_L @ self.prev_s_hat + self.steady_L @ self.yt
        return s_hat

    def predict_lls(self):
        t = len(self.measurement_history)
        yt_vector = []
        # constructing measurement vector
        for yt in self.measurement_history:
            yt_vector.append(yt.item())
            for _ in range(self.dim):
                yt_vector.append(0)
        yt_vector = np.array(yt_vector[:-1 * self.dim])  # drop extra 0 vector appended to end by loop

        # constructing A
        A_n_rows = yt_vector.shape[0]
        A_n_columns = t * self.dim
        A = np.zeros((A_n_rows, A_n_columns))
        negative_I = -1 * np.eye(
            self.dim)  # note that this identity matrix has different dimensions from the one used for gain

        A[0, 0:2] = self.H  # base case
        for i in range(t - 1):
            x_offset = self.dim * i
            y_offset = i * 3 + 1  # 3 because y has dim 1, state has dim
            A[y_offset: y_offset + 2, x_offset: x_offset + 2] = self.F
            A[y_offset: y_offset + 2, x_offset + 2: x_offset + 4] = negative_I
            A[y_offset + 2, x_offset + 2: x_offset + 4] = self.H

        s_hats = np.linalg.pinv(A.T @ A) @ A.T @ yt_vector
        return s_hats[-2:]

    # 1) storesz new true state and filtered measurement in object, does not make a new state prediction
    # 2) updates all histories
    def update_system(self):
        system_noise = self.get_system_noise()
        measurement_noise = self.get_measurement_noise()

        self.st = self.F @ self.st + system_noise
        self.filtered_y = self.H @ self.st
        self.yt = self.filtered_y + measurement_noise

        self.noise_history.append(system_noise)
        self.noise_history.append(measurement_noise)
        self.state_history.append(self.st)
        self.measurement_history.append(self.yt)
        self.filtered_y_history.append(self.filtered_y)
        self.L_history.append(self.gain())

    # #returns observed state, measurement + true state, measurement
    # def system_vars(self):
    #   return self.st, self.filtered_y, self.yt

    def get_trajectory(self, time_steps):
        s_hats, s_hats_steady, s_hats_lls = [], [], []
        for _ in range(time_steps):
            s_hat = self.predict_kalman()
            s_hat_steady = self.predict_steady_kalman()
            s_hat_lls = self.predict_lls()
            s_hats_lls.append(s_hat_lls)
            s_hats.append(s_hat)
            s_hats_steady.append(s_hat_steady)
            self.update_system()
            self.prev_s_hat = s_hat

        return s_hats, s_hats_steady, s_hats_lls

    def get_trajectories(self, initial_states, time_steps):
        trajectories = []
        for x0 in initial_states:
            self.curr_state = x0
            sts, filtered_ys, s_hats, yts = self.get_trajectory_kalman(time_steps)
            trajectory = [sts, filtered_ys, s_hats, yts]
            trajectories.append(trajectory)

        return trajectories

