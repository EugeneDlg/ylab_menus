import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(".env")
TEST_MODE = os.getenv("TEST_MODE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
DB_CONN_STRING_PRE = "postgresql+asyncpg"
DB_CONN_STRING = (
    f"{DB_CONN_STRING_PRE}://{DB_USER}:{DB_PASSWORD}@" f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
TEST_DB_CONN_STRING = (
    f"{DB_CONN_STRING_PRE}://{TEST_DB_USER}:"
    f"{TEST_DB_PASSWORD}@{TEST_DB_HOST}:"
    f"{DB_PORT}/{TEST_DB_NAME}"
)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_CACHE_TIME = int(os.getenv("REDIS_CACHE_TIME", 300))
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

BASE_URL = "http://localhost:8000"
BASE_DIR = Path(__file__).resolve().parent.parent
