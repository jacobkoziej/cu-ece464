# SPDX-License-Identifier: GPL-3.0-or-later
#
# __init__.py -- db management
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import importlib.resources
import sqlite3

from os import PathLike
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

    def add_action(self, action: Action) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            "INSERT INTO actions(name, command) VALUES (:name, :command)",
            action.model_dump(),
        )

        self.connection.commit()

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
