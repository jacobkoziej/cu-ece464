# SPDX-License-Identifier: GPL-3.0-or-later
#
# __main__.py -- main
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import sys

from argparse import ArgumentParser


def main() -> None:
    parser = ArgumentParser(
        description="jankins client",
    )

    parser.add_argument(
        "-a",
        "--address",
        default="",
        help="server address",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--port",
        default=4640,
        help="server port",
        type=int,
    )

    args = parser.parse_args()

    _ = args


if __name__ == "__main__":
    sys.exit(main())
