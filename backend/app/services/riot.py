import os, httpx
from app.cache import get_cached, set_cached
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
REGION = os.getenv("RIOT_REGION", "na1")
HEADERS = {"X-Riot-Token": API_KEY}
BASE_URL = f"https://{REGION}.api.riotgames.com/tft"

if not API_KEY:
    raise RuntimeError("Missing RIOT_API_KEY in environment")

_client = httpx.AsyncClient(
    headers={"X-Riot-Token": API_KEY},
    timeout=10.0
)

async def fetch_riot(path: str, params: dict = None):
    resp = await _client.get(f"{BASE_URL}{path}", params=params)
    resp.raise_for_status()
    return resp.json()

async def _cached_fetch(cache_key: str, fetcher, ttl: int):
    if data := await get_cached(cache_key):
        return data
    data = await fetcher()
    await set_cached(cache_key, data, ttl=ttl)
    return data

async def get_latest_dd_version() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get("https://ddragon.leagueoflegends.com/api/versions.json")
        r.raise_for_status()
        versions = r.json()
    return versions[0]

async def get_champions():
    async def fetcher():
        version = await get_latest_dd_version()
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-champion.json"
        resp = await _client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:champions", fetcher, ttl=7*24*3600)

async def get_items():
    async def fetcher():
        version = await get_latest_dd_version()
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-item.json"
        resp = await _client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:items", fetcher, ttl=7*24*3600)

async def get_traits():
    async def fetcher():
        version = await get_latest_dd_version()
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-trait.json"
        resp = await _client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:traits", fetcher, ttl=7*24*3600)

async def get_augments():
    async def fetcher():
        version = await get_latest_dd_version()
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-augments.json"
        resp = await _client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:augments", fetcher, ttl=7*24*3600)