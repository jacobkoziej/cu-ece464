# SPDX-License-Identifier: GPL-3.0-or-later
#
# serial.py -- serial functions
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from typing import Any

from pydantic import BaseModel

from . import message


def decode(obj: Any) -> Any:
    if "__model__" in obj:
        return getattr(message, obj["__model__"]).model_validate(
            obj["__dump__"],
        )

    return obj


def encode(obj: Any) -> Any:
    if isinstance(obj, BaseModel):
        return {
            "__model__": obj.__class__.__name__,
            "__dump__": obj.model_dump(),
        }

    return obj
