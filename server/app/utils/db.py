import httpx

from app.config import DB_URL

# Database client
db = httpx.Client(base_url=DB_URL)
