import zipfile
from pathlib import Path

FONT_PATH = Path("./font/")
BDF_PATH = Path("./bdf/")

FONT_PATH.mkdir(parents=True, exist_ok=True)
BDF_PATH.mkdir(parents=True, exist_ok=True)


def extract_bdf_from_zipfile(zf: zipfile.ZipFile):
    bdf_file_names = filter(lambda x: x.endswith(".bdf"), zf.namelist())
    for file_name in bdf_file_names:
        zf.extract(file_name, BDF_PATH)


for zip_file_name in FONT_PATH.glob("*.zip"):
    with zipfile.ZipFile(zip_file_name, "r") as zf:
        extract_bdf_from_zipfile(zf)
