import socket
import os
import time


def server_start():
    SOCKET_PATH = "/sockets/cicd.sock"

    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(1)
    print({time.time()}, "Waiting for connection...")

    conn, _ = server.accept()
    print({time.time()}, "Client connected")

    return server, conn


def server_recv(conn):
    data = conn.recv(1024)
    if not data:
        print("Client disconnected")
        return "quit"

    msg = data.decode()

    return msg


def server_send(conn, msg):
    conn.sendall(msg.encode())


def server_close(server, conn):
    conn.close()
    server.close()

    time.sleep(2)


if __name__ == "__main__":
    server, conn = server_start()

    while True:
        msg = server_recv(conn)
        if msg == "quit":
            break

        server_send(conn, msg)

    server_close(server, conn)
