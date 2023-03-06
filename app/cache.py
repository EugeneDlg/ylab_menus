from json import dumps, loads

import aioredis
from fastapi.encoders import jsonable_encoder

from app.envconfig import REDIS_CACHE_TIME, REDIS_URL


class Cache:
    def __init__(self):
        self.session: aioredis.Redis = aioredis.from_url(url=REDIS_URL)

    async def get_cache(self, key):
        value = await self.session.get(name=key)
        return loads(value) if value else None

    async def set_cache(self, key, value):
        json_value = jsonable_encoder(value)
        await self.session.set(name=key, value=dumps(json_value), ex=REDIS_CACHE_TIME)

    async def delete_cache(self, key, bulk=False):
        if bulk:
            prefix = key
            cur = b"0"  # set initial cursor to 0
            while cur:
                cur, keys = await self.session.scan(cur, match=f"{prefix}*")
                for key in keys:
                    await self.session.delete(key)
        else:
            await self.session.delete(key)

    async def clean_cache(self):
        await self.session.flushall()


async def get_cache():
    cache = Cache()
    return cache
