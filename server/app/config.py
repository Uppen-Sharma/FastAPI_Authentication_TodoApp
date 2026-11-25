import os
import httpx
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Signing algorithm
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Access token secret
ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET_KEY")

# Access token life (minutes)
ACCESS_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Refresh token secret
REFRESH_SECRET = os.getenv("REFRESH_TOKEN_SECRET_KEY")

# Refresh token life (days)
REFRESH_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Max session length (days)
SESSION_MAX_DAYS = int(os.getenv("SESSION_MAX_DAYS", "7"))

# Allowed frontends
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()]

# Database URL
DB_URL = os.getenv("DB_URL", "http://localhost:4000")

# True only on HTTPS
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"

# Login and register limit
AUTH_RATE_LIMIT = os.getenv("AUTH_RATE_LIMIT", "5/minute")

# Grace period for old sessions
REFRESH_GRACE_SECONDS = int(os.getenv("REFRESH_GRACE_SECONDS", "10"))

# Database client
db = httpx.Client(base_url=DB_URL)
