import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN", "")

PG_USER = os.getenv("PG_USER", "")
PG_HOST = os.getenv("PG_HOST", "")
PG_DATABASE_NAME = os.getenv("PG_DATABASE_NAME", "")

OWNER_ID = int(os.getenv('OWNER_ID', 0))
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
