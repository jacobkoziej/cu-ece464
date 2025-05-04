# SPDX-License-Identifier: GPL-3.0-or-later
#
# message.py -- message definitions
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

from typing import Optional

from pydantic import BaseModel


class Action(BaseModel):
    name: str
    command: str


class ActionResponse(BaseModel):
    action_id: Optional[int] = None
    error: Optional[str] = None


class Authenticate(BaseModel):
    username: str
    passwd: str


class GenericFailure(BaseModel):
    reason: Optional[str] = None


class JobEnd(BaseModel):
    job_id: int
    return_code: int
    artifact: bytes


class JobStart(BaseModel):
    job_id: Optional[int]


class JobStartResponse(BaseModel):
    job_id: Optional[int] = None
    command: Optional[str] = None
    error: Optional[str] = None


class Queue(BaseModel):
    action_id: int


class QueueResponse(BaseModel):
    job_id: Optional[int] = None
    error: Optional[str] = None
