# SPDX-License-Identifier: GPL-3.0-or-later
#
# config.py -- config
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from pydantic import BaseModel


class Config(BaseModel):
    username: str
    password: str
    hostname: str = "localhost"
    port: int = 4640
