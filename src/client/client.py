from . import *
import socket
import time
import random


def client_connect():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)

    return client


def client_send(client, task, value):
    msg = task + " " + str(value)
    print("Send: ", msg)

    client.sendall(msg.encode())


def client_recv(client, task):
    msg = client.recv(1024).decode()
    print("Received: ", msg)

    return msg


def client_disconnect(client):
    client.close()


def generate_point(i):
    return (XRange[1]-XRange[0])*random.random() + XRange[0]


if __name__ == "__main__":
    time.sleep(1)

    client = client_connect()
    time.sleep(0.5)

    try:
        client_send(client, "c", "64")
        # client_send(client, "l", "test.save")
        # time.sleep(0.5)
        #
        # for i in range(5):
        #     point = generate_point(i)
        #
        #     client_send(client, "i", point)
        #     time.sleep(0.1)
        #
        #     value = client_recv(client, "i")
        #     time.sleep(0.1)

    except BrokenPipeError:
        print("Connection was closed")

    client_disconnect(client)
