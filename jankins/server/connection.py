# SPDX-License-Identifier: GPL-3.0-or-later
#
# connection.py -- connection handler
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import socket

from socketserver import (
    BaseRequestHandler,
    TCPServer,
    ThreadingMixIn,
)
from typing import Optional

from loguru import logger

from ..message import (
    Action,
    ActionResponse,
    Authenticate,
    GenericFailure,
    JobStart,
    JobStartResponse,
    Queue,
    QueueResponse,
)
from ..serial import (
    rx,
    tx,
)
from .config import Config
from .db import Database


class Handler(BaseRequestHandler):
    config: Optional[Config]

    def _failure(self, error: Optional[str] = None) -> None:
        response = GenericFailure(error=error)

        if error is None:
            error = "unspecified generic failure"

        logger.error(error)

        tx(self.request, [response])

    def _handle_Action(self, uid: int, action: Action) -> None:
        response = ActionResponse()

        try:
            response.action_id = self.db.add_action(action)

            logger.success(f"added action: {action.name}")

        except Exception:
            response.error = f"failed to add action: {action.name}"

            logger.error(response.error)

        finally:
            tx(self.request, [response])

    def _handle_JobStart(self, uid: int, job_start: JobStart) -> None:
        response = JobStartResponse()

        try:
            response.job_id, action_id = self.db.delegate_job(
                uid,
                job_start.job_id,
            )
            response.command = self.db.action_id_to_command(action_id)

            if response.command is None:
                raise KeyError

            logger.success(f"started job: {response.job_id}")

        except Exception:
            response.error = "failed to start job"

            logger.error(f"{response.error}: {job_start.job_id}")

        finally:
            tx(self.request, [response])

    def _handle_Queue(self, uid: int, queue: Queue) -> None:
        response = QueueResponse()

        try:
            response.job_id = self.db.pend_job(queue.action_id)

            logger.success(f"queued action as job: {response.job_id}")

        except Exception:
            response.error = "failed to queue action"

            logger.error(f"{response.error}: {queue.action_id}")

        finally:
            tx(self.request, [response])

    def setup(self) -> None:
        self.db = Database(self.config.user_data_path / "database.sqlite")

    def handle(self) -> None:
        sock = self.request
        config = self.config

        logger.info(f"got connection: {sock.getpeername()}")

        msgs = rx(sock, config.recieve_bufsize)
        sock.shutdown(socket.SHUT_RD)

        if not msgs:
            self._failure("got no messages")
            return

        auth = msgs.popleft()

        if not isinstance(auth, Authenticate) or not (
            uid := self.db.authenticate(auth)
        ):
            self._failure(f"authentication failed for user: {auth.username}")
            return

        logger.success(f"authenticated user: {auth.username}")

        sub_command = msgs.popleft()
        sub_command_handler = getattr(
            self,
            f"_handle_{type(sub_command).__name__}",
            None,
        )

        if sub_command_handler is None:
            self._failure("unknown sub-command encountered")
            return

        sub_command_handler(uid, sub_command)

    def finish(self) -> None:
        del self.db


class Server(ThreadingMixIn, TCPServer):
    allow_reuse_address = True
