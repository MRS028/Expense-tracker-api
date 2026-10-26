import os
from dotenv import load_dotenv

load_dotenv(override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please add it to your .env file (copy from Supabase → Connect → Session pooler)."
    )