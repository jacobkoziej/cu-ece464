# SPDX-License-Identifier: GPL-3.0-or-later
#
# __main__.py -- main
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import sys

import yaml

from argparse import ArgumentParser
from pathlib import Path


def main() -> None:
    parser = ArgumentParser(
        description="jankins server",
    )

    parser.add_argument(
        "--config",
        default="config.yaml",
        help="checkpoint path",
        metavar="config.yaml",
        type=Path,
    )

    args = parser.parse_args()

    with open(args.config) as fp:
        config = yaml.safe_load(fp)

    _ = config


if __name__ == "__main__":
    sys.exit(main())
