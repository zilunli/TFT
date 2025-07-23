import os, httpx
from app.cache import get_cached, set_cached

API_KEY = os.getenv("RIOT_API_KEY")
ACCOUNT_REGION = os.getenv("RIOT_REGION", "americas")
GAME_REGION = os.getenv("GAME_REGION", "na1")
HEADERS = {"X-Riot-Token": API_KEY}
REGION_URL = f"https://{ACCOUNT_REGION}.api.riotgames.com"
GAME_URL = f"https://{GAME_REGION}.api.riotgames.com"

if not API_KEY:
    raise RuntimeError("Missing RIOT_API_KEY in environment")

_region_client = httpx.AsyncClient(
    base_url=REGION_URL,
    headers={"X-Riot-Token": API_KEY},
    timeout=10.0
)
_game_client = httpx.AsyncClient(
    base_url=GAME_URL,
    headers={"X-Riot-Token": API_KEY},
    timeout=10.0
)

async def fetch_riot_region(path: str, params: dict = None):
    resp = await _region_client.get(path, params=params)
    resp.raise_for_status()
    return resp.json()

async def fetch_riot_game(path: str, params: dict = None):
    resp = await _game_client.get(path, params=params)
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
        resp = await _game_client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:champions", fetcher, ttl=7*24*3600)

async def get_items():
    async def fetcher():
        version = await get_latest_dd_version()
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-item.json"
        resp = await _game_client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:items", fetcher, ttl=7*24*3600)

async def get_traits():
    async def fetcher():
        version = await get_latest_dd_version()
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-trait.json"
        resp = await _game_client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:traits", fetcher, ttl=7*24*3600)

async def get_augments():
    async def fetcher():
        version = await get_latest_dd_version()
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-augments.json"
        resp = await _game_client.get(url)
        resp.raise_for_status()
        return resp.json()["data"]
    return await _cached_fetch("static:augments", fetcher, ttl=7*24*3600)

async def get_account_by_gamename_and_tagline(gameName: str, tagLine: str):
    cache_key = f"account:{gameName}{tagLine}"
    async def fetcher():
        return await fetch_riot_region(f"/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}")
    return await _cached_fetch(cache_key, fetcher, ttl=60 * 60)

async def get_summoner_by_puuid(puuid: str):
    cache_key = f"summoner:puuid{puuid}"
    async def fetcher():
        return await fetch_riot_game(f"/tft/summoner/v1/summoners/by-puuid/{puuid}")
    return await _cached_fetch(cache_key, fetcher, ttl=60 * 60)

async def get_history_by_puuid(puuid: str, start: int = 0, count: int = 20):
    cache_key = f"history:{puuid}"
    async def fetcher():
        return await fetch_riot_region(
            f"/tft/match/v1/matches/by-puuid/{puuid}/ids",
            params={"start": start, "count": count}
        )
    return await _cached_fetch(cache_key, fetcher, ttl=60 * 60)

async def get_match_by_match_id(match_id: str):
    cache_key = f"match:{match_id}"
    async def fetcher():
        return await fetch_riot_region(f"/tft/match/v1/matches/{match_id}")
    return await _cached_fetch(cache_key, fetcher, ttl=7 * 24 * 3600)
