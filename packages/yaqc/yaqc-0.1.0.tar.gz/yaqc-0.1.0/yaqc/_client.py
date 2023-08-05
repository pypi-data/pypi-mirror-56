__all__ = ["Client", "YaqDaemonException"]


import functools
import socket
import json


BUFFSIZE = 4096


class YaqDaemonException(Exception):
    pass


def reconnect(fun):
    """
    If the socket link is broken, try creating a new link and run the method again.
    """

    @functools.wraps(fun)
    def inner(self, *args, **kwargs):
        try:
            return fun(self, *args, **kwargs)
        except ConnectionError:
            self.connect_socket()
            return fun(self, *args, **kwargs)

    return inner


class Client:
    def __init__(self, port, host="127.0.0.1"):
        self._host = host
        self._port = port
        self.connect_socket()
        self._id_counter = 0

        methods = self.send("list_methods")
        for c, d in zip(methods, self.send("help", methods)):
            if hasattr(self, c):
                continue

            def fun(comm):
                return lambda *args, **kwargs: self.send(comm, *args, **kwargs)

            setattr(self, c, fun(c))
            getattr(self, c).__doc__ = d

    def connect_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    def help(self, method=None):
        print(self.send("help", method))

    @reconnect
    def send(self, method, *args, **kwargs):
        message = {"jsonrpc": "2.0", "method": method, "id": self._id_counter}
        self._id_counter += 1
        if args and kwargs:
            # TODO, this should be resolvable once the idea of "signature" is in the spec
            # At which point, all args can be inserted into the kwarg dict
            raise YaqDaemonException(
                "Cannot pass both positional and keyword arguments"
            )
        if args:
            message["params"] = args
        elif kwargs:
            message["params"] = kwargs
        self._socket.sendall(json.dumps(message).encode())
        message = self._socket.recv(BUFFSIZE)
        message = json.loads(message)
        if "error" in message:
            raise YaqDaemonException(
                f"{message['error']['code']}: {message['error']['message']}"
            )
        if "result" in message:
            return message["result"]
