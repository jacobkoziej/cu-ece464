# SPDX-License-Identifier: GPL-3.0-or-later
#
# __main__.py -- main
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import sys

import yaml

from argparse import ArgumentParser
from pathlib import Path

from .config import Config


def main() -> None:
    parser = ArgumentParser(
        description="jankins server",
    )

    parser.add_argument(
        "--config",
        default="",
        help="checkpoint path",
        metavar="config.yaml",
        type=Path,
    )

    args = parser.parse_args()

    if args.config.is_file():
        with open(args.config) as fp:
            config = yaml.safe_load(fp)

    else:
        config = {}

    config = Config.model_validate(config)


if __name__ == "__main__":
    sys.exit(main())
