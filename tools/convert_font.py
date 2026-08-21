#!/usr/bin/env python3

import re
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.progress import track

bdfconv = "bdfconv.exe" if sys.platform.startswith("win32") else "bdfconv"
BDF_DIR = Path("bdf")
SRC_DIR = Path("src")

BDF_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

console = Console()


def extract_ranges(path: Path) -> list[str]:
    codes = set()
    with open(path, encoding="latin1") as f:
        for line in f:
            m = re.match(r"ENCODING (-?\d+)", line)
            if m and (code := int(m.group(1))) >= 0:
                codes.add(code)

    codes = sorted(codes)
    ranges = []
    start = prev = codes[0]

    for code in codes[1:]:
        if code != prev + 1:
            ranges.append(f"{start}-{prev}" if start != prev else str(start))
            start = code
        prev = code

    ranges.append(f"{start}-{prev}" if start != prev else str(start))
    return ranges


def main():
    for bdf_file in track(
        list(BDF_DIR.glob("*.bdf")),
        description="converting...",
        console=console,
    ):
        ranges = extract_ranges(bdf_file)

        font_name = bdf_file.stem.replace("-", "_")
        variable_name = f"u8g2_font_{font_name}"
        c_path = (SRC_DIR / font_name).with_suffix(".c")

        subprocess.run(
            [
                f"./tools/{bdfconv}",
                "-f",
                "1",
                "-m",
                ",".join(ranges),
                "-n",
                variable_name,
                "-o",
                str(c_path),
                str(bdf_file),
            ],
            check=True,
        )

        console.log(f"converted {bdf_file} -> {c_path}.")


if __name__ == "__main__":
    main()
