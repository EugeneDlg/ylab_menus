from json import dumps, loads

import aioredis
from fastapi.encoders import jsonable_encoder

from app.envconfig import REDIS_CACHE_TIME, REDIS_URL

cache = aioredis.from_url(url=REDIS_URL)


async def get_cache(key):
    value = await cache.get(name=key)
    return loads(value) if value else None


async def set_cache(key, value):
    json_value = jsonable_encoder(value)
    await cache.set(name=key, value=dumps(json_value), ex=REDIS_CACHE_TIME)


async def delete_cache(key, bulk=False):
    if bulk:
        prefix = key
        cur = b'0'  # set initial cursor to 0
        while cur:
            cur, keys = await cache.scan(cur, match=f"{prefix}*")
            for key in keys:
                await cache.delete(key)
    else:
        await cache.delete(key)


async def clean_cache():
    await cache.flushall()
