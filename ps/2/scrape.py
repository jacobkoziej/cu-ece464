#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# scape.py -- scraper for <https://quotes.toscrape.com/>
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import argparse
import sys

import requests

from http import HTTPStatus
from typing import Final
from itertools import count


_BASE_URL: Final[str] = "https://quotes.toscrape.com"


def main() -> None:
    argparser = argparse.ArgumentParser(
        description="scraper for <https://quotes.toscrape.com/>",
    )

    argparser.add_argument(
        "-p",
        "--pages",
        help="pages to scrape",
        metavar="N",
        type=int,
    )

    args = argparser.parse_args()

    pages = count(1) if args.pages is None else range(1, args.pages + 1)

    for i in pages:
        url = _BASE_URL + f"/page/{i}/"

        request = requests.get(url)

        if request.status_code != HTTPStatus.OK:
            sys.exit(f"<{url}> status: {request.status_code}")


if __name__ == "__main__":
    sys.exit(main())
