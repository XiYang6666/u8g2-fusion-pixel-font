from pathlib import Path

BDF_DIR = Path("bdf")
HEADER_FILE_PATH = Path("include/u8g2_fusion_pixel_font.h")
HEADER_TEMPLATE_PREFIX = """
#pragma once
#include <stdint.h>

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


variables = []
for file_path in BDF_DIR.glob("*.bdf"):
    file_name = file_path.stem
    variables.append(f"u8g2_font_{file_name.replace('-', '_')}")

with open(HEADER_FILE_PATH, "w", encoding="utf-8") as f:
    f.write(HEADER_TEMPLATE_PREFIX)
    f.write("\n")
    f.writelines(f'extern const uint8_t {variable}[] U8G2_FONT_SECTION("{variable}");\n' for variable in variables)
    f.write(HEADER_TEMPLATE_SUFFIX)
