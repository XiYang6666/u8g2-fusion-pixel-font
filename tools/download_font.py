#!/usr/bin/env python3

import asyncio
import re
from collections.abc import Callable
from pathlib import Path

from httpx import AsyncClient
from rich.console import Console
from rich.progress import Progress

FONT_DIR = Path("font")
FONT_DIR.mkdir(parents=True, exist_ok=True)

client = AsyncClient()
console = Console()


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


async def download_file(url: str, path: Path, *, done_cb: Callable):
    response = await client.get(url, follow_redirects=True)
    response.raise_for_status()
    await asyncio.to_thread(path.write_bytes, response.content)
    done_cb()


async def download_files(files_map: dict[str, str], *, done_cb: Callable):
    tasks = [
        download_file(url, FONT_DIR / file_name, done_cb=done_cb)
        for file_name, url in files_map.items()
    ]
    await asyncio.gather(*tasks)


async def main():
    console.log("fetching release info...")
    files_map = await get_release_files()
    console.log("starting font file download.")
    with Progress(console=console) as progress:
        task = progress.add_task("downloading...", total=len(files_map))
        await download_files(
            files_map,
            done_cb=lambda: progress.update(task, advance=1),
        )
    console.log("done.")


if __name__ == "__main__":
    asyncio.run(main())
