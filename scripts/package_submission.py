#!/usr/bin/env python3
"""Create and verify the minimal Kaggle submission archive."""

import argparse
import gzip
import io
import tarfile
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY_ROOT / "main.py"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "dist" / "submission.tar.gz"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )
    return parser.parse_args()


def create_submission(source, output):
    """Build a byte-reproducible archive without host identity metadata."""
    if not source.is_file():
        raise FileNotFoundError(source)

    source_bytes = source.read_bytes()
    compile(source_bytes.decode("utf-8"), str(source), "exec")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw_archive:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw_archive,
            compresslevel=9,
            mtime=0,
        ) as compressed_archive:
            with tarfile.open(
                mode="w",
                fileobj=compressed_archive,
                format=tarfile.USTAR_FORMAT,
            ) as archive:
                member = tarfile.TarInfo("main.py")
                member.size = len(source_bytes)
                member.mode = 0o644
                member.mtime = 0
                member.uid = 0
                member.gid = 0
                member.uname = ""
                member.gname = ""
                archive.addfile(member, io.BytesIO(source_bytes))

    with tarfile.open(output, "r:gz") as archive:
        members = archive.getmembers()
    if (
        len(members) != 1
        or members[0].name != "main.py"
        or not members[0].isfile()
    ):
        raise RuntimeError(
            f"unexpected archive members: {[member.name for member in members]}"
        )

    size = output.stat().st_size
    if size > 100 * 1024 * 1024:
        raise RuntimeError(f"submission exceeds 100 MiB: {size} bytes")
    return size


def main():
    args = parse_args()
    output = args.output if args.output.is_absolute() else Path.cwd() / args.output
    size = create_submission(SOURCE, output)
    print(f"{output} ({size} bytes): main.py")


if __name__ == "__main__":
    main()
