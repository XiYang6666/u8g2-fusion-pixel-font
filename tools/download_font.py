import asyncio
import re
from pathlib import Path

from httpx import AsyncClient

FONT_DIR = Path("font")
FONT_DIR.mkdir(parents=True, exist_ok=True)

client = AsyncClient()


async def get_release_files() -> dict[str, str]:
    url = "https://api.github.com/repos/TakWolf/fusion-pixel-font/releases/latest"
    response = await client.get(url)
    response.raise_for_status()

    files_map = {}
    for asset in response.json()["assets"]:
        if re.match(
            r"fusion-pixel-font-(8|10|12)px-(monospaced|proportional)-bdf-v(.*).zip",
            asset["name"],
        ):
            files_map[asset["name"]] = asset["browser_download_url"]
    return files_map


async def download_file(url: str, path: Path):
    response = await client.get(url, follow_redirects=True)
    response.raise_for_status()
    with open(path, "wb") as f:
        f.writelines(response.iter_bytes(chunk_size=4096))


async def download_files(files_map: dict[str, str]):
    tasks = [
        download_file(url, FONT_DIR / file_name) for file_name, url in files_map.items()
    ]
    await asyncio.gather(*tasks)


async def main():
    files_map = await get_release_files()
    await download_files(files_map)


if __name__ == "__main__":
    asyncio.run(main())
