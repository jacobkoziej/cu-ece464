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
from importlib import import_module
from pathlib import Path

from loguru import logger
from platformdirs import user_config_dir

from .. import message
from ..message import (
    Action,
    Authenticate,
    Queue,
)
from ..serial import (
    rx,
    tx,
)
from .config import Config


def _action(args: Namespace, config: Config) -> int:
    return _generic(args, config)


def _generic(args: Namespace, config: Config) -> int:
    sock = _config2sock(config)

    logger.debug(f"connecting to {sock.getpeername()}")

    auth = _config2auth(config)

    logger.debug(f"authenticating as: {auth.username}")

    module = import_module(__name__)
    out = getattr(module, f"_args2{args.sub_command}")(args)

    tx(sock, [auth, out])
    sock.shutdown(socket.SHUT_WR)

    msgs = rx(sock)

    if not msgs:
        logger.error("got no response from server")
        sock.close()
        return 1

    response = msgs.popleft()

    dtype = getattr(message, f"{args.sub_command.capitalize()}Response")

    if not isinstance(response, dtype):
        logger.error("got incorrect respone")
        sock.close()
        return 1

    if response.error:
        logger.error(response.error)

    else:
        logger.success(f"transaction complete: {response}")

    sock.close()

    return int(not response.error)


def _args2action(args: Namespace) -> Action:
    return Action(name=args.name, command=args.command)


def _args2queue(args: Namespace) -> Action:
    return Queue(action_id=args.action_id)


def _config2sock(config: Config) -> socket.socket:
    return socket.create_connection((config.hostname, config.port))


def _config2auth(config: Config) -> Authenticate:
    return Authenticate(username=config.username, passwd=config.passwd)


def _config2queue(config: Config) -> Queue:
    return Queue(action_id=config.action_id)


def _queue(args: Namespace, config: Config) -> int:
    return _generic(args, config)


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
        "-c",
        "--command",
        help="action command",
        required=True,
        type=str,
    )
    action_parser.add_argument(
        "-n",
        "--name",
        help="action name",
        required=True,
        type=str,
    )

    queue_parser = subparsers.add_parser("queue")
    queue_parser.add_argument(
        "-i",
        "--action-id",
        help="action id",
        required=True,
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

    return sub_command(args, config)


if __name__ == "__main__":
    sys.exit(main())
