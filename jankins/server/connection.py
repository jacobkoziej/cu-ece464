# SPDX-License-Identifier: GPL-3.0-or-later
#
# connection.py -- connection handler
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from socketserver import (
    BaseRequestHandler,
    TCPServer,
    ThreadingMixIn,
)
from typing import Optional

from loguru import logger
from msgpack import Unpacker

from ..serial import decode
from .config import Config


class Handler(BaseRequestHandler):
    config: Optional[Config]

    def setup(self) -> None: ...

    def handle(self) -> None:
        sock = self.request
        config = self.config

        logger.info(f"got connection: {sock.getpeername()}")

        unpacker = Unpacker(object_hook=decode)

        while True:
            buf = sock.recv(config.recieve_bufsize)

            if not buf:
                break

            unpacker.feed(buf)

            for msg in unpacker:
                logger.info(msg)

    def finish(self) -> None: ...


class Server(ThreadingMixIn, TCPServer):
    pass
