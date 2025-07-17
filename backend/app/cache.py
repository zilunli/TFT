import os, json
import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")
redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_cached(key: str):
    data = await redis_client.get(key)
    return json.loads(data) if data else None

async def set_cached(key: str, value: dict, ttl: int):
    await redis_client.set(key, json.dumps(value), ex=ttl)
