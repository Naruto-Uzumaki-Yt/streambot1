import os

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

DB_URL = os.getenv("DB_URL", "")
BASE_URL = os.getenv("BASE_URL", "")

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
