# SPDX-License-Identifier: GPL-3.0-or-later
#
# __main__.py -- main
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import socket
import sys

import yaml

from argparse import ArgumentParser
from pathlib import Path

from platformdirs import user_config_dir
from loguru import logger

from .config import Config


def main() -> None:
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

    address = (config.hostname, config.port)

    logger.debug(f"connecting to {address}")

    sock = socket.create_connection(address)

    sock.close()


if __name__ == "__main__":
    sys.exit(main())
