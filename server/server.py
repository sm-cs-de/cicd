import socket
import os
import time

SOCKET_PATH = "/sockets/cicd.sock"

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)
print({time.time()}, "Waiting for connection...")

conn, _ = server.accept()
print({time.time()}, "Client connected")

while True:
    data = conn.recv(1024)
    if not data:
        print("Client disconnected")
        break
    message = data.decode()

    if message == "quit":
        break
    else:
        conn.sendall(message)

conn.close()
server.close()

time.sleep(2)
