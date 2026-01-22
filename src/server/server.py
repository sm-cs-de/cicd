from . import *
import socket
import os
import time
import re
import ann
import torch.nn as nn


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
        return "quit", "Client disconnect"

    msg = data_.decode()

    rgx = "([i,l,s]+)\\s+(.+)"
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
    interpolator = None

    while True:
        task, data = server_recv(conn)

        msg = ""
        quit = False
        if task == "quit":
            msg = task + data
            quit = True
        elif task == "l":
            msg = "loading.." # https://apxml.com/courses/getting-started-with-pytorch/chapter-6-implementing-training-loop/saving-loading-model-checkpoints
            ###
        elif task == "s":
            if not interpolator:
                msg = "no model"
                quit = True
            else:
                msg = "saving.."
                ###
        elif task == "c":
            msg = "creating.."
            interpolator = ann.Interpolator(1, [64,64], nn.ReLU)
                ###
        elif task == "t":
            if not interpolator:
                msg = "no model"
                quit = True
            else:
                msg = "training.."
                ###
        elif task == "i":
            if not interpolator:
                msg = "no model"
                quit = True
            else:
                msg = interpolator.forward(float(data))

        print({time.time()}, msg)
        if quit:
            break
        else:
            server_send(conn, msg)

    server_close(server, conn)
