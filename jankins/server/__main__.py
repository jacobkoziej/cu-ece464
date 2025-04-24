# SPDX-License-Identifier: GPL-3.0-or-later
#
# __main__.py -- main
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import sys

import yaml

from argparse import ArgumentParser
from pathlib import Path
from threading import Thread

from .config import Config
from .connection import (
    Handler,
    Server,
)

from loguru import logger


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
        logger.info(f"reading config from `{args.config.resolve()}`")

        with open(args.config) as fp:
            config = yaml.safe_load(fp)

    else:
        config = {}

    config = Config.model_validate(config)

    logger.info(f"starting server on port {config.port}")

    with Server(("", config.port), Handler) as server:
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True

        try:
            server_thread.start()
            logger.success(
                f"server thread started with thread id {server_thread.native_id}"
            )

            server_thread.join()
            logger.critical("server thread exited unexpectedly")

        except KeyboardInterrupt:
            logger.warning("caught KeyboardInterrupt, gracefully exiting")

        except Exception:
            logger.exception("caught unknown exception, gracefully exiting")

        finally:
            server.shutdown()
            server_thread.join()
            logger.success("server thread exited")


if __name__ == "__main__":
    sys.exit(main())
