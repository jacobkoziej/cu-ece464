# SPDX-License-Identifier: GPL-3.0-or-later
#
# __init__.py -- server
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from . import (
    config,
    work,
)

from loguru import logger as _logger

__all__ = [
    "config",
    "work",
]

_logger.disable("client")
