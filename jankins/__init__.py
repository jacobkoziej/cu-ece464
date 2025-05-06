# SPDX-License-Identifier: GPL-3.0-or-later
#
# __init__.py -- jankins
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from . import (
    client,
    message,
    serial,
    server,
)
from ._version import (
    __version__,
    __version_tuple__,
)

__all__ = [
    "__version__",
    "__version_tuple__",
    "client",
    "message",
    "serial",
    "server",
]
