from . import *
import os
import torch
import torch.nn as nn
import torch.optim as optim
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
        self.input_dim = input_dim
        self.dim = int(input_dim-1)//2


    def scale(self, data, range):
        return (data - range[0]) / (range[1] - range[0])


    def unscale(self, data, range):
        return data * (range[1] - range[0]) + range[0]


    def forward(self, x):
        ret = self.model(self.scale(x, XRange)).squeeze(-1)

        return self.unscale(ret, YRange)


    def train_batch(self, x, y, optimizer, loss_fn):
        optimizer.zero_grad()
        pred = self.forward(x)
        loss = loss_fn(self.scale(pred, YRange), self.scale(y, YRange))
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


    def load(self, path: str):
        state = torch.load(path, map_location=torch.device("cpu"))
        self.load_state_dict(state)


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
        self.rnd = np.random.default_rng()


    def generate_function(self, n_points: int):
        xs = np.sort(self.rnd.uniform(*XRange, size=n_points))
        ys = np.sin(xs) + self.rnd.normal(0, RndScale, size=n_points)
        f = self.MODES[self.mode](xs, ys)

        return xs, ys, f


    def generate_dataset(self, count: int, n_points: int) -> Tuple[torch.tensor, torch.tensor]:
        x = []
        y = []

        for _ in range(count):
            xs, ys, f = self.generate_function(n_points)

            inter_x = self.rnd.uniform(xs.min(), xs.max())
            inter_y = float(f(inter_x))

            ann_input = np.concatenate([xs, ys, [inter_x]])
            x.append(ann_input)
            y.append(inter_y)

        return torch.tensor(np.array(x,dtype=np.float32)), torch.tensor(np.array(y,dtype=np.float32))
