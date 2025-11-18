import socket
import time


def client_connect():
    SOCKET_PATH = "/sockets/cicd.sock"

    time.sleep(1)
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)


def client_send(value):
    msg = str(value)
    client.sendall(msg.encode())


def client_recv():
    msg = client.recv(1024).decode()
    value = float(msg)

    return value


def client_disconnect():
    client.close()


if __name__ == "__main__":
    client_connect()

    i = 0
    while i<10:
        point = 2.1 + 0.1*i
        client_send(point)

        value = client_recv()
        print(value)

        i += 1

    client_disconnect()
