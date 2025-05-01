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

from ..message import (
    Action,
    Authenticate,
    Success,
)
from ..serial import (
    rx,
    tx,
)
from .config import Config
from .db import Database


class Handler(BaseRequestHandler):
    config: Optional[Config]

    def _handle_Action(self, uid: int, action: Action) -> bool:
        try:
            self.db.add_action(action)

        except Exception:
            logger.error(f"failed to add action: {action.name}")
            return False

        logger.success(f"added action: {action.name}")

        return True

    def _return_success(self, success: bool) -> None:
        tx(self.request, [Success(success=success)])

    def setup(self) -> None:
        self.db = Database(self.config.database_path)

    def handle(self) -> None:
        sock = self.request
        config = self.config

        logger.info(f"got connection: {sock.getpeername()}")

        msgs = rx(sock, config.recieve_bufsize)

        if not msgs:
            logger.warning("got no messages")
            self._return_success(False)
            return

        auth = msgs.popleft()

        if not isinstance(auth, Authenticate) or not (
            uid := self.db.authenticate(auth)
        ):
            logger.warning(f"authentication failed for user: {auth.username}")
            self._return_success(False)
            return

        logger.success(f"authenticated user: {auth.username}")

        sub_command = msgs.popleft()
        sub_command_handler = getattr(
            self,
            f"_handle_{type(sub_command).__name__}",
            None,
        )

        if sub_command_handler is None:
            logger.error("unknown sub-command encountered")
            self._return_success(False)
            return

        success = sub_command_handler(uid, sub_command)

        self._return_success(success)

    def finish(self) -> None:
        del self.db


class Server(ThreadingMixIn, TCPServer):
    allow_reuse_address = True
