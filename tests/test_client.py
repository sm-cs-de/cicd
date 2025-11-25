import os
import math
import unittest
from unittest.mock import patch, MagicMock

import src.client.client as unit


# self.assertEqual(a, b)
# self.assertNotEqual(a, b)
# self.assertTrue(expr)
# self.assertFalse(expr)
# self.assertIsNone(x)
# self.assertIn(item, container)
# self.assertRaises(ExceptionType, func, *args)


class TestGeneratePoint(unittest.TestCase):
    def setUp(self):
        self.lower_bound = 0.0
        self.upper_bound = 10.0
        self.i_min = 0
        self.i_max = 10

    def test_lower_bound(self):
        self.assertTrue(unit.generate_point(self.i_min) >= self.lower_bound)

    def test_upper_bound(self):
        self.assertTrue(unit.generate_point(self.i_max) <= self.upper_bound)


class TestSocket(unittest.TestCase):
    @patch("client.client.socket.socket")
    @patch("client.client.time.sleep")

    def test_client_connect(self, mock_sleep, mock_socket_class):
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket

        SOCKET_PATH = "/sockets/cicd.sock"
        s = unit.client_connect()

        mock_sleep.assert_called_once()
        mock_socket_class.assert_called_once_with(unit.socket.AF_UNIX, unit.socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(SOCKET_PATH)

        self.assertEqual(s, mock_socket)

    def test_client_send(self):
        mock_socket = MagicMock()

        value = 123
        unit.client_send(mock_socket, value)
        mock_socket.sendall.assert_called_once_with(b"123")

    def test_client_recv_float(self):
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b"1.23"

        result = unit.client_recv(mock_socket)
        mock_socket.recv.assert_called_once_with(1024)
        self.assertEqual(result, 1.23)

    def test_client_recv_invalid(self):
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b"nan"

        result = unit.client_recv(mock_socket)
        mock_socket.recv.assert_called_once_with(1024)
        self.assertTrue(math.isnan(result))

    def test_client_disconnect(self):
        mock_socket = MagicMock()

        unit.client_disconnect(mock_socket)
        mock_socket.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
