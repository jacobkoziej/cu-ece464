# SPDX-License-Identifier: GPL-3.0-or-later
#
# config.py -- config
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from pydantic import BaseModel


class Config(BaseModel):
    port: int = 4640
    recieve_bufsize: int = 1024
