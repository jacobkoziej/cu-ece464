# SPDX-License-Identifier: GPL-3.0-or-later
#
# serial.py -- serial functions
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import socket

from collections import deque
from typing import Any

from msgpack import (
    Packer,
    Unpacker,
)
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


def rx(sock: socket.socket, bufsize: int = 1024) -> deque[Any]:
    msgs = deque()

    unpacker = Unpacker(object_hook=decode)

    while True:
        buf = sock.recv(bufsize)

        if not buf:
            break

        unpacker.feed(buf)

        for msg in unpacker:
            msgs.append(msg)

    return msgs


def tx(sock: socket.socket, objs: list[Any]) -> None:
    packer = Packer(default=encode)

    for obj in objs:
        sock.sendall(packer.pack(obj))
