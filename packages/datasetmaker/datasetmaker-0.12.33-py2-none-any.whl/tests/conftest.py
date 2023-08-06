"""Make sure internet is disabled when running tests."""

import socket


class block_network(socket.socket):
    def __init__(self, *args, **kwargs):
        raise Exception('Network call blocked')


socket.socket = block_network
