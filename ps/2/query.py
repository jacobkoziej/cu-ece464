#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# query.py -- query for <https://quotes.toscrape.com/> database
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import argparse
import json
import sys

from pathlib import Path


def main() -> None:
    argparser = argparse.ArgumentParser(
        description="query for <https://quotes.toscrape.com/> database",
    )

    argparser.add_argument(
        "-a",
        "--authors",
        default=[],
        help="authors to query",
        metavar="AUTHOR",
        nargs="*",
        type=str,
    )
    argparser.add_argument(
        "-d",
        "--database",
        default=Path("quotes.json"),
        help="output path",
        metavar="quotes.json",
        type=Path,
    )
    argparser.add_argument(
        "-t",
        "--tags",
        default=[],
        help="tags to query",
        metavar="TAG",
        nargs="*",
        type=str,
    )

    args = argparser.parse_args()

    authors = set(args.authors)
    tags = set(args.tags)

    with open(args.database) as f:
        database = json.load(f)

    query = []

    for entry in database:
        if authors and entry["author"] not in authors:
            continue

        for tag in entry["tags"]:
            if tag in tags:
                break

        else:
            if tags:
                continue

        query.append(entry)

    print(json.dumps(query, indent=4))


if __name__ == "__main__":
    sys.exit(main())
