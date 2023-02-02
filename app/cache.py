import redis
from json import dumps, loads
from fastapi.encoders import jsonable_encoder
from app.config import REDIS_URL


REDIS_CACHE_TIME = 300


class Cache:
    def __init__(self, session):
        self.session = session

    def get_cache(self, key):
        value = self.session.get(name=key)
        return loads(value) if value else None

    def set_cache(self, key, value):
        json_value = jsonable_encoder(value)
        self.session.set(name=key, value=dumps(json_value), ex=REDIS_CACHE_TIME)

    def delete_cache(self, key, bulk=False):
        if bulk:
            prefix = key
            for key in self.session.scan_iter(f"{prefix}*"):
                self.session.delete(key)
        else:
            self.session.delete(key)

    def clean_cache(self):
        self.session.flushall()


def get_cache_session():
    session = redis.from_url(
        url=REDIS_URL, encoding='utf-8', decode_responses=True,
    )
    yield session
