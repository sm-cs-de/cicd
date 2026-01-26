from . import *
import torch
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np
from typing import List, Callable, Tuple
from scipy.interpolate import interp1d, CubicSpline, PchipInterpolator


class Interpolator(nn.Module):
    def __init__(self, input_dim: int, hidden_layers: List[int], activation: Callable = nn.ReLU):
        super().__init__()

        layers = []
        last_dim = input_dim
        for h in hidden_layers:
            layers.append(nn.Linear(last_dim, h))
            layers.append(activation())
            last_dim = h
        layers.append(nn.Linear(last_dim, 1))

        self.model = nn.Sequential(*layers)


    def forward(self, x):
        return self.model(x).squeeze(-1)


    def train_batch(self, x, y, optimizer, loss_fn):
        optimizer.zero_grad()
        pred = self.forward(x)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()

        return loss.item()


    def train_full(self, x, y, lr=1e-3, epochs=100, batch_size=64):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        loss_fn = nn.MSELoss()

        dataset = torch.utils.data.TensorDataset(x, y)
        loader  = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

        for _ in range(epochs):
            for bx, by in loader:
                self.train_batch(bx, by, optimizer, loss_fn)


    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.state_dict(), path)


    @staticmethod
    def load(path: str, input_dim: int, hidden_layers: List[int], activation: Callable = nn.ReLU):
        model = Interpolator(input_dim, hidden_layers, activation)
        state = torch.load(path, map_location=torch.device("cpu"))
        model.load_state_dict(state)

        return model



class TrainingData:
    MODES = {
        "linear": lambda xs, ys: interp1d(xs, ys, kind="linear", fill_value="extrapolate"),
        "cubic": lambda xs, ys: CubicSpline(xs, ys),
        "pchip": lambda xs, ys: PchipInterpolator(xs, ys),
    }


    def __init__(self, mode: str):
        if mode not in self.MODES:
            raise ValueError(f"Unknown interpolation mode '{mode}'")
        self.mode = mode


    def generate_function(self, n_points: int):
        xs = np.sort(np.random.uniform(*XRange, size=n_points))
        ys = np.sin(xs) + np.random.normal(0, RndScale, size=n_points)
        f = self.MODES[self.mode](xs, ys)

        return xs, ys, f


    def generate_dataset(self, count: int, n_points: int) -> Tuple[torch.tensor, torch.tensor]:
        X = []
        Y = []

        for _ in range(count):
            xs, ys, f = self.generate_function(n_points)

            inter_x = np.random.uniform(xs.min(), xs.max())
            inter_y = float(f(inter_x))

            ann_input = np.concatenate([xs, ys, [inter_x]])
            X.append(ann_input)
            Y.append(inter_y)

        return torch.tensor(np.array(X,dtype=np.float32)), torch.tensor(np.array(Y,dtype=np.float32))
