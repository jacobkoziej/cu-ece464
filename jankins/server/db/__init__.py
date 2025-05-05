# SPDX-License-Identifier: GPL-3.0-or-later
#
# __init__.py -- db management
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import importlib.resources
import sqlite3

from os import PathLike
from time import time_ns
from typing import Optional

from ...message import (
    Action,
    Authenticate,
)


class Database:
    def __del__(self) -> None:
        self.connection.close()

    def __init__(
        self,
        path: PathLike,
        *,
        timeout: float = 5.0,
        autocommit: bool = False,
        create_tables: bool = False,
    ) -> None:
        self.connection = sqlite3.connect(
            database=path,
            timeout=timeout,
            autocommit=autocommit,
        )
        self.connection.commit()

        if create_tables:
            script = (
                importlib.resources.files(__package__) / "tables.sql"
            ).read_text()

            self.connection.executescript(script)
            self.connection.commit()

    def action_id_valid(self, action_id: int) -> bool:
        cursor = self.connection.cursor()

        result = cursor.execute(
            "SELECT active FROM actions WHERE id = ?", (action_id,)
        ).fetchone()

        self.connection.commit()

        if result is None:
            return False

        active = bool(result[0])

        return active

    def add_action(self, action: Action) -> int:
        cursor = self.connection.cursor()

        id = cursor.execute(
            "INSERT INTO actions(name, command) VALUES (:name, :command) RETURNING id",
            action.model_dump(),
        ).fetchone()[0]

        self.connection.commit()

        return id

    def authenticate(self, auth: Authenticate) -> Optional[int]:
        cursor = self.connection.cursor()

        result = cursor.execute(
            "SELECT id FROM users WHERE username = :username AND passwd = :passwd",
            auth.model_dump(),
        )

        if id := result.fetchone():
            id = id[0]

        self.connection.commit()

        return id

    def job_states(self) -> dict[str, int]:
        cursor = self.connection.cursor()

        result = cursor.execute("SELECT name, value FROM job_state")

        states = dict(result.fetchall())

        self.connection.commit()

        return states

    def delegate_job(
        self,
        uid: int,
        job_id: Optional[int] = None,
    ) -> Optional[int]:
        states = self.job_states()

        cursor = self.connection.cursor()

        if job_id is None:
            job_id = cursor.execute(
                "SELECT id FROM jobs WHERE state = ?",
                (states["PENDING"],),
            ).fetchone()

            if not job_id:
                return None

            job_id = job_id[0]

        parameters = {
            "id": job_id,
            "owner": uid,
            "start_time": time_ns(),
            "state": states["RUNNING"],
        }

        cursor.execute(
            "UPDATE jobs "
            "SET owner = :owner, start_time = :start_time, state = :state "
            "WHERE id = :id",
            parameters,
        )

        self.connection.commit()

        return job_id

    def pend_job(self, action_id: int) -> Optional[int]:
        if not self.action_id_valid(action_id):
            return None

        states = self.job_states()

        cursor = self.connection.cursor()

        id = cursor.execute(
            "INSERT INTO jobs(action, state) VALUES (?, ?) RETURNING id",
            (action_id, states["PENDING"]),
        ).fetchone()[0]

        self.connection.commit()

        return id
