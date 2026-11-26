import httpx

from app.config import DB_URL

# Database client
database = httpx.Client(base_url=DB_URL)
