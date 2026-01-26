import torch

from . import *
from . import ann
import socket
import os
import time
import re
import torch.nn as nn
import numpy as np


def server_start():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(3)
    print({time.time()}, "Waiting for connection...")

    conn, _ = server.accept()
    print({time.time()}, "Client connected")

    return server, conn


def server_recv(conn):
    data_ = conn.recv(1024)
    if not data_:
        return "quit", "IO error"

    msg = data_.decode()
    if msg == "quit":
        return "quit", "Client disconnect"

    rgx = "([c,i,l,s]+)\\s+(.+)"
    match = re.findall(rgx, msg)
    if not match:
        return "quit", "Invalid message"
    else:
        task = match[0][0]
        data = match[0][1]

        return task, data


def server_send(conn, msg):
    conn.sendall(msg.encode())


def server_close(server, conn):
    conn.close()
    server.close()

    time.sleep(2)


if __name__ == "__main__":
    server, conn = server_start()
    inter = None

    while True:
        task, data = server_recv(conn)

        msg = ""
        quit = False
        if task == "quit":
            msg = data
            quit = True
        elif task == "l":
            msg = "loading.." # https://apxml.com/courses/getting-started-with-pytorch/chapter-6-implementing-training-loop/saving-loading-model-checkpoints
            ###
        elif task == "s":
            if not inter:
                msg = "no model"
                quit = True
            else:
                msg = "saving.."
                ###
        elif task == "c":
            dim = int(data)
            msg = "creating ANN with " + str(2*dim+1) + " inputs for " + str(dim) + " points and the x-position"

            inter = ann.Interpolator(2*dim+1, [64, 64], nn.ReLU)
            train = ann.TrainingData("linear")
            train_data_x, train_data_y = train.generate_dataset(500, dim)
            inter.train_full(train_data_x, train_data_y)

            x_sample = np.sort(np.random.uniform(*XRange, size=dim))
            y_sample = np.sin(x_sample)
            x_inter = 0.0
            ann_input = torch.tensor(np.concatenate([x_sample, y_sample, [x_inter]]),dtype=torch.float32)
            print(inter(ann_input))

        elif task == "t":
            if not inter:
                msg = "no model"
                quit = True
            else:
                msg = "training.."
                ###
        elif task == "i":
            if not inter:
                msg = "no model"
                quit = True
            else:
                msg = inter.forward(float(data))

        print({time.time()}, "quit: "+msg if quit else msg)
        if quit:
            break
        else:
            server_send(conn, msg)

    server_close(server, conn)
