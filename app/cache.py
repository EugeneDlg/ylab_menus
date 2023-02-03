import aioredis
from json import dumps, loads
from fastapi.encoders import jsonable_encoder
from app.config import REDIS_URL

# cache = redis.from_url(url=REDIS_URL, encoding='utf-8', decode_responses=True)
cache = aioredis.from_url(url=REDIS_URL)

REDIS_CACHE_TIME = 300


async def get_cache(key):
    value = await cache.get(name=key)
    return loads(value) if value else None


async def set_cache(key, value):
    json_value = jsonable_encoder(value)
    await cache.set(name=key, value=dumps(json_value), ex=REDIS_CACHE_TIME)


async def delete_cache(key, bulk=False):
    if bulk:
        prefix = key
        for key in cache.scan_iter(f"{prefix}*"):
            await cache.delete(key)
    else:
        await cache.delete(key)


async def clean_cache():
    await cache.flushall()
