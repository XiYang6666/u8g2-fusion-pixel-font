import re
import subprocess
import sys
from pathlib import Path

bdfconv = "bdfconv.exe" if sys.platform.startswith("win32") else "bdfconv"
BDF_DIR = Path("bdf")
SRC_DIR = Path("src")

BDF_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

for bdf_file in BDF_DIR.glob("*.bdf"):
    codes = set()

    with open(bdf_file, encoding="latin1") as f:
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

    print(f"{bdf_file} -> {c_path}")
