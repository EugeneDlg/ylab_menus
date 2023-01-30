import redis
from json import dumps, loads
from fastapi.encoders import jsonable_encoder
from app.config import REDIS_URL

cache = redis.from_url(url=REDIS_URL, encoding='utf-8', decode_responses=True)

REDIS_CACHE_TIME = 300


def get_cache(key):
    value = cache.get(name=key)
    return loads(value) if value else None


def set_cache(key, value):
    json_value = jsonable_encoder(value)
    cache.set(name=key, value=dumps(json_value), ex=REDIS_CACHE_TIME)


def delete_cache(key, bulk=False):
    if bulk:
        prefix = key
        for key in cache.scan_iter(f"{prefix}*"):
            cache.delete(key)
    else:
        cache.delete(key)


def clean_cache():
    cache.flushall()
