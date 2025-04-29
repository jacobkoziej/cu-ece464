# SPDX-License-Identifier: GPL-3.0-or-later
#
# connection.py -- connection handler
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from collections import deque
from socketserver import (
    BaseRequestHandler,
    TCPServer,
    ThreadingMixIn,
)
from typing import Optional

from loguru import logger
from msgpack import Unpacker

from ..message import (
    Authenticate,
)
from ..serial import decode
from .config import Config
from .db import Database


class Handler(BaseRequestHandler):
    config: Optional[Config]

    def setup(self) -> None:
        self.db = Database(self.config.database_path)

    def handle(self) -> None:
        sock = self.request
        config = self.config

        logger.info(f"got connection: {sock.getpeername()}")

        unpacker = Unpacker(object_hook=decode)

        msgs = deque()

        while True:
            buf = sock.recv(config.recieve_bufsize)

            if not buf:
                break

            unpacker.feed(buf)

            for msg in unpacker:
                msgs.append(msg)

        if not msgs:
            logger.warn("got no messages")
            return

        auth = msgs.popleft()

        if not isinstance(auth, Authenticate) or not (
            uid := self.db.authenticate(auth)
        ):
            logger.warning(f"authentication failed for user: {auth.username}")
            return

        logger.success(f"authenticated user: {auth.username}")

        _ = uid

    def finish(self) -> None:
        del self.db


class Server(ThreadingMixIn, TCPServer):
    pass
