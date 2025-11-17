import socket
import time

SOCKET_PATH = "/sockets/cicd.sock"

time.sleep(1)
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect(SOCKET_PATH)

i = 0
while i<10:
    point = 2.1

    msg = str(point)
    client.sendall(msg.encode())

    reply = client.recv(1024).decode()
    print(reply)

    i += 1

client.close()

