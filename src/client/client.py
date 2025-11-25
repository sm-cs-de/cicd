import socket
import time
import math


def client_connect():
    SOCKET_PATH = "/sockets/cicd.sock"

    time.sleep(1)
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)

    return client


def client_send(client, value):
    msg = str(value)
    client.sendall(msg.encode())


def client_recv(client):
    msg = client.recv(1024).decode()
    try:
        value = float(msg)
    except ValueError:
        value = math.nan

    return value


def client_disconnect(client):
    client.close()


def generate_point(i):
    return 0.1 * i


if __name__ == "__main__":
    client = client_connect()

    point = generate_point(0)
    for i in range(10):
        client_send(client, point)

        value = client_recv(client)
        print(value)

        i += 1
        point = generate_point(i)
        time.sleep(0.25)

    client_disconnect(client)
