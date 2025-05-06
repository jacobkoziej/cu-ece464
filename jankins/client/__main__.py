# SPDX-License-Identifier: GPL-3.0-or-later
#
# __main__.py -- main
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import socket
import sys

import yaml

from argparse import (
    ArgumentParser,
    Namespace,
)
from concurrent.futures import ThreadPoolExecutor
from importlib import import_module
from pathlib import Path
from typing import Optional

from loguru import logger
from platformdirs import user_config_dir
from pydantic import BaseModel

from .. import message
from ..message import (
    Action,
    Authenticate,
    JobStart,
    Queue,
    Stat,
)
from ..serial import (
    rx,
    tx,
)
from .config import Config
from .work import handle_job


def _action(args: Namespace, config: Config) -> BaseModel:
    return _generic(args, config)


def _generic(
    args: Namespace,
    config: Config,
    model: Optional[str] = None,
    out: Optional[BaseModel] = None,
    success: bool = True,
) -> BaseModel:
    if model is None:
        model = args.sub_command.capitalize()

    sock = _config2sock(config)

    logger.debug(f"connecting to {sock.getpeername()}")

    auth = _config2Auth(config)

    logger.debug(f"authenticating as: {auth.username}")

    module = import_module(__name__)

    if out is None:
        out = getattr(module, f"_args2{model}")(args)

    tx(sock, [auth, out])
    sock.shutdown(socket.SHUT_WR)

    msgs = rx(sock)

    if not msgs:
        logger.error("got no response from server")
        sock.close()
        return 1

    response = msgs.popleft()

    dtype = getattr(message, f"{model}Response")

    if not isinstance(response, dtype):
        logger.error("got incorrect respone")
        sock.close()
        return 1

    if response.error:
        logger.error(response.error)

    else:
        if success:
            logger.success(f"transaction complete: {response}")

    sock.close()

    return response


def _args2Action(args: Namespace) -> Action:
    return Action(name=args.name, command=args.command)


def _args2JobStart(args: Namespace) -> JobStart:
    return JobStart(job_id=args.job_id)


def _args2Queue(args: Namespace) -> Action:
    return Queue(action_id=args.action_id)


def _args2Stat(args: Namespace) -> Stat:
    return Stat(state=args.state)


def _config2sock(config: Config) -> socket.socket:
    return socket.create_connection((config.hostname, config.port))


def _config2Auth(config: Config) -> Authenticate:
    return Authenticate(username=config.username, passwd=config.passwd)


def _queue(args: Namespace, config: Config) -> BaseModel:
    return _generic(args, config)


def _stat(args: Namespace, config: Config) -> BaseModel:
    response = _generic(args, config, success=False)

    if not response.error:
        logger.success(response.stats)


def _work(args: Namespace, config: Config) -> BaseModel:
    response = _generic(args, config, model="JobStart")

    if response is None or response.error:
        return response

    args.job_id = response.job_id

    with ThreadPoolExecutor() as executor:
        future = executor.submit(handle_job, response)

        out = future.result(timeout=None)

    return _generic(args, config, model="JobEnd", out=out)


def main() -> int:
    parser = ArgumentParser(
        description="jankins client",
    )

    parser.add_argument(
        "--config",
        default=Path(user_config_dir("jankins")) / "config.yaml",
        help="checkpoint path",
        metavar="config.yaml",
        type=Path,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable verbose logging",
    )

    subparsers = parser.add_subparsers(
        dest="sub_command",
        required=True,
    )

    action_parser = subparsers.add_parser("action")
    action_parser.add_argument(
        "--command",
        help="action command",
        required=True,
        type=str,
    )
    action_parser.add_argument(
        "--name",
        help="action name",
        required=True,
        type=str,
    )

    queue_parser = subparsers.add_parser("queue")
    queue_parser.add_argument(
        "--action-id",
        help="action id",
        required=True,
        type=int,
    )

    stat_parser = subparsers.add_parser("stat")
    stat_parser.add_argument(
        "--state",
        choices=[
            "COMPLETE",
            "PENDING",
            "RUNNING",
            "TIMEOUT",
        ],
        default="PENDING",
        help="state",
        type=str,
    )

    work_parser = subparsers.add_parser("work")
    work_parser.add_argument(
        "--job-id",
        help="job id",
        type=int,
    )

    args = parser.parse_args()

    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>",
        level="TRACE" if args.verbose else "INFO",
    )

    logger.debug(f"reading config from `{args.config.resolve()}`")

    with open(args.config) as fp:
        config = yaml.safe_load(fp)

    config = Config.model_validate(config)

    module = import_module(__name__)
    sub_command = getattr(module, f"_{args.sub_command}")

    response = sub_command(args, config)

    if response is None:
        return 1

    return 1 if response.error else 0


if __name__ == "__main__":
    sys.exit(main())
