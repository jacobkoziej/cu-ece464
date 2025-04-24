# SPDX-License-Identifier: GPL-3.0-or-later
#
# __init__.py -- server
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from . import (
    config,
    connection,
)

from loguru import logger as _logger

__all__ = [
    "config",
    "connection",
]

_logger.disable("server")
