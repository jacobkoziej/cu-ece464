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
from .db import Database

from loguru import logger
from platformdirs import user_data_dir


def main() -> None:
    parser = ArgumentParser(
        description="jankins server",
    )

    parser.add_argument(
        "--config",
        default=Path("config.yaml"),
        help="checkpoint path",
        metavar="config.yaml",
        type=Path,
    )

    args = parser.parse_args()

    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</green> | "
        "<blue>{process}:{thread}</blue> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>",
    )

    if args.config.is_file():
        logger.info(f"reading config from `{args.config.resolve()}`")

        with open(args.config) as fp:
            config = yaml.safe_load(fp)

    else:
        config = {}

    Handler.config = config = Config.model_validate(config)

    if config.user_data_path is None:
        config.user_data_path = Path(
            user_data_dir("jankins", ensure_exists=True)
        )

    config.user_data_path = Path(config.user_data_path)

    database_path = config.user_data_path / "database.sqlite"

    logger.info(f"using database at `{database_path.resolve()}`")

    db = Database(database_path, create_tables=True)

    logger.info(f"starting server on port {config.port}")

    with Server(("", config.port), Handler) as server:
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True

        try:
            server_thread.start()
            logger.success(
                f"server thread started with id {server_thread.ident}"
            )

            while True:
                server_thread.join(timeout=10)

                logger.debug("pruning timed-out running jobs")

                db.timeout_running()

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
