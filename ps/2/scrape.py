#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# scape.py -- scraper for <https://quotes.toscrape.com/>
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import argparse
import json
import sys

import requests

from dataclasses import (
    asdict,
    dataclass,
)
from http import HTTPStatus
from itertools import count
from pathlib import Path
from typing import (
    Final,
    Optional,
)

from bs4 import BeautifulSoup
from bs4.element import Tag


_BASE_URL: Final[str] = "https://quotes.toscrape.com"


@dataclass(frozen=True)
class Quote:
    author: str
    text: str
    tags: list[str]


def clean_text(text: str) -> str:
    return text.strip().strip("“”")


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
    argparser.add_argument(
        "-o",
        "--output",
        default=Path("quotes.json"),
        help="output path",
        metavar="quotes.json",
        type=Path,
    )

    args = argparser.parse_args()

    pages = count(1) if args.pages is None else range(1, args.pages + 1)

    quotes = []

    for i in pages:
        url = _BASE_URL + f"/page/{i}/"

        request = requests.get(url)

        if request.status_code != HTTPStatus.OK:
            sys.exit(f"<{url}> status: {request.status_code}")

        soup = BeautifulSoup(request.content, "html.parser")

        if not (div_quotes := soup.select("div.quote")):
            break

        print(f"page: {i:02d}")

        quotes += [asdict(parse_quote(quote)) for quote in div_quotes]

    with open(args.output, "w") as f:
        f.write(json.dumps(quotes, indent=4))
        f.write("\n")


def parse_quote(quote: Tag) -> Optional[Quote]:
    if not (author := quote.find_all(class_="author")):
        return None

    author = clean_text(author[0].text)

    if not (text := quote.find_all(class_="text")):
        return None

    text = clean_text(text[0].text)

    tags = [clean_text(tag.text) for tag in quote.find_all(class_="tag")]

    return Quote(author, text, tags)


if __name__ == "__main__":
    sys.exit(main())
