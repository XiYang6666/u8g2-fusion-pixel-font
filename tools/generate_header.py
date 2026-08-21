#!/usr/bin/env python3

import re
from pathlib import Path

from rich.console import Console

BDF_DIR = Path("bdf")
HEADER_FILE_PATH = Path("include/u8g2_fusion_pixel_font.h")
HEADER_TEMPLATE_PREFIX = """
#pragma once
#include <stdint.h>

#ifndef U8G2_USE_LARGE_FONTS
#define U8G2_USE_LARGE_FONTS
#endif

#ifndef U8G2_FONT_SECTION
#define U8G2_FONT_SECTION(name)
#endif

#ifdef __cplusplus
extern "C" {
#endif

#ifdef U8G2_USE_LARGE_FONTS
""".strip()

HEADER_TEMPLATE_SUFFIX = """
#endif

#ifdef __cplusplus
}
#endif
""".strip()

BDF_DIR.mkdir(parents=True, exist_ok=True)
HEADER_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)


console = Console()


def main():
    console.log("generating header file...")
    variables = []
    for file_path in BDF_DIR.glob("*.bdf"):
        file_name = file_path.stem
        variables.append(file_name.replace("-", "_"))
    pattern = re.compile(r"fusion_pixel_(\d+)px_(?:.*)_(?:.*)")
    variables.sort(key=lambda x: (int(pattern.match(x).group(1)), x))
    variables = [f"u8g2_font_{x}" for x in variables]

    with open(HEADER_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(HEADER_TEMPLATE_PREFIX)
        f.write("\n")
        f.writelines(
            f'extern const uint8_t {variable}[] U8G2_FONT_SECTION("{variable}");\n'
            for variable in variables
        )
        f.write(HEADER_TEMPLATE_SUFFIX)
    console.log("done.")


if __name__ == "__main__":
    main()
