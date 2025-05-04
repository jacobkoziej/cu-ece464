# SPDX-License-Identifier: GPL-3.0-or-later
#
# work.py -- handle work jobs
# Copyright (C) 2025  Jacob Koziej <jacobkoziej@gmail.com>

import subprocess

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import (
    ZIP_DEFLATED,
    ZipFile,
)

from ..message import (
    JobStartResponse,
    JobEnd,
)


def handle_job(response: JobStartResponse) -> JobEnd:
    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)

        stdout = open(tmp_dir / "stdout.txt", "w")
        stderr = open(tmp_dir / "stderr.txt", "w")
        outdir = tmp_dir / "out"

        outdir.mkdir(parents=True, exist_ok=True)

        complete = subprocess.run(
            response.command,
            stdout=stdout,
            stderr=stderr,
            shell=True,
            cwd=outdir,
        )

        stdout.close()
        stderr.close()

        buffer = BytesIO()

        with ZipFile(buffer, "w", ZIP_DEFLATED) as zip_file:
            for root, _, files in tmp_dir.walk():
                for file in files:
                    path = root / file
                    zip_file.write(path, path.relative_to(tmp_dir))

    return JobEnd(
        job_id=response.job_id,
        return_code=complete.returncode,
        artifact=buffer.getvalue(),
    )
