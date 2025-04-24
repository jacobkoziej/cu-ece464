# SPDX-License-Identifier: GPL-3.0-or-later
#
# connection.py -- connection handler
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from socketserver import (
    BaseRequestHandler,
    TCPServer,
    ThreadingMixIn,
)


class Handler(BaseRequestHandler):
    def setup(self) -> None: ...

    def handle(self) -> None: ...

    def finish(self) -> None: ...


class Server(ThreadingMixIn, TCPServer):
    pass
