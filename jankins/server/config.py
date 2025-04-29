# SPDX-License-Identifier: GPL-3.0-or-later
#
# config.py -- config
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from os import PathLike
from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    database_path: Optional[PathLike] = None
    port: int = 4640
    recieve_bufsize: int = 1024
