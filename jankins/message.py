# SPDX-License-Identifier: GPL-3.0-or-later
#
# message.py -- message definitions
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from pydantic import BaseModel


class Authenticate(BaseModel):
    username: str
    passwd: str
