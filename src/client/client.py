from . import *
import socket
import time
import numpy as np


def client_connect():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)

    return client


def client_send(client, task, value):
    if len(str(value)) > 0:
        msg = task + " " + str(value)
    else:
        msg = task
    print("Send: ", msg)

    client.sendall(msg.encode())


def client_recv(client, task):
    msg = client.recv(1024).decode()
    print("Received: ", msg)

    return msg


def client_disconnect(client):
    client.close()


def generate_point(rnd, i):
    return (XRange[1]-XRange[0])*rnd.random() + XRange[0]


if __name__ == "__main__":
    time.sleep(3)

    client = client_connect()
    time.sleep(0.5)

    try:
        client_send(client, "c", "20")
        client_recv(client, "c")

        client_send(client, "t", "1000")
        client_recv(client, "t")
        time.sleep(0.5)

        client_send(client, "s", "test.sav")
        time.sleep(0.5)

        client_send(client, "l", "test.sav")
        time.sleep(0.5)

        rnd = np.random.default_rng()
        for i in range(5):
            point = generate_point(rnd, i)
            client_send(client, "i", point)
            value = client_recv(client, "i")
            time.sleep(0.1)

        client_send(client, "quit", "")
        client_recv(client, "")

    except BrokenPipeError:
        print("Connection was closed")

    client_disconnect(client)
