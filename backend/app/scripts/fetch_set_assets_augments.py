import os
import asyncio
import httpx
from pathlib import Path

# Config
OUTPUT_DIR = Path(__file__).parent.parent / "assets" / "augments"
VERSION_URL        = "https://ddragon.leagueoflegends.com/api/versions.json"
DATA_URL_TEMPLATE  = "https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-augments.json"
IMG_URL_TEMPLATE   = "https://ddragon.leagueoflegends.com/cdn/{version}/img/{group}/{filename}"
HTTP_TIMEOUT       = 10.0  # seconds

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.get(VERSION_URL)
        resp.raise_for_status()
        version = resp.json()[0]
        print(f"Using Data Dragon version: {version}")

        data_url = DATA_URL_TEMPLATE.format(version=version)
        resp = await client.get(data_url)
        resp.raise_for_status()
        augments = resp.json()["data"]

        files_to_download = [
            info["image"]["full"]
            for info in augments.values()
            if info["image"]["full"]
        ]
        print(f"Found {len(files_to_download)} Set Augment")

        tasks = []
        for filename in files_to_download:
            url  = IMG_URL_TEMPLATE.format(
                       version=version,
                       group="tft-augment",
                       filename=filename
                   )
            dest = OUTPUT_DIR / filename
            tasks.append(_download(client, url, dest))

        await asyncio.gather(*tasks)

async def _download(client: httpx.AsyncClient, url: str, dest: Path):
    resp = await client.get(url)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    print(f"Saved {dest.name}")

if __name__ == "__main__":
    asyncio.run(main())