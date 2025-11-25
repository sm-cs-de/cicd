import os
import time
import unittest
from unittest.mock import patch, MagicMock

import src.server.server as unit


class TestServer(unittest.TestCase):
    @patch("server.server.socket.socket")
    @patch("server.server.os.remove")
    @patch("server.server.os.path.exists")
    @patch("server.server.time.time")
    def test_server_start(self, mock_time, mock_exists, mock_remove, mock_socket_class):
        mock_exists.return_value = True
        mock_socket = MagicMock()
        mock_conn = MagicMock()

        mock_socket_class.return_value = mock_socket
        mock_socket.accept.return_value = (mock_conn, None)
        mock_time.return_value = 123.456

        server, conn = unit.server_start()
        SOCKET_PATH = "/sockets/cicd.sock"

        mock_exists.assert_called_once_with(SOCKET_PATH)
        mock_remove.assert_called_once_with(SOCKET_PATH)

        mock_socket_class.assert_called_once_with(unit.socket.AF_UNIX, unit.socket.SOCK_STREAM)
        mock_socket.bind.assert_called_once_with(SOCKET_PATH)
        mock_socket.listen.assert_called_once_with(1)
        mock_socket.accept.assert_called_once()

        self.assertEqual(server, mock_socket)
        self.assertEqual(conn, mock_conn)

    def test_server_recv_data(self):
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b"hello"

        result = unit.server_recv(mock_conn)
        mock_conn.recv.assert_called_once_with(1024)
        self.assertEqual(result, "hello")

    def test_server_recv_empty(self):
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b""  # simulate client disconnect

        result = unit.server_recv(mock_conn)
        mock_conn.recv.assert_called_once_with(1024)
        self.assertEqual(result, "quit")  # expected quit message

    def test_server_send(self):
        mock_conn = MagicMock()

        unit.server_send(mock_conn, "test")
        mock_conn.sendall.assert_called_once_with(b"test")

    @patch("server.server.time.sleep")
    def test_server_close(self, mock_sleep):
        mock_server = MagicMock()
        mock_conn = MagicMock()

        unit.server_close(mock_server, mock_conn)
        mock_conn.close.assert_called_once()
        mock_server.close.assert_called_once()

        mock_sleep.assert_called_once_with(2)


if __name__ == "__main__":
    unittest.main()
