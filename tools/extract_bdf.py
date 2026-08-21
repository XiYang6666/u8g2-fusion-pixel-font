#!/usr/bin/env python3

import zipfile
from pathlib import Path

from rich.console import Console
from rich.progress import track

FONT_PATH = Path("./font/")
BDF_PATH = Path("./bdf/")

FONT_PATH.mkdir(parents=True, exist_ok=True)
BDF_PATH.mkdir(parents=True, exist_ok=True)

console = Console()


def extract_bdf_from_zipfile(zf: zipfile.ZipFile):
    bdf_file_names = filter(lambda x: x.endswith(".bdf"), zf.namelist())
    for file_name in bdf_file_names:
        zf.extract(file_name, BDF_PATH)


def main():
    console.log("extracting files...")
    for zip_file_name in track(
        list(FONT_PATH.glob("*.zip")),
        "extracting...",
        console=console,
    ):
        with zipfile.ZipFile(zip_file_name, "r") as zf:
            extract_bdf_from_zipfile(zf)
    console.log("done.")


if __name__ == "__main__":
    main()
