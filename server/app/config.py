import os
import httpx
from dotenv import load_dotenv

# Read the settings from server/.env
load_dotenv()

# Algorithm used to sign both tokens
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Secret that signs access tokens
ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET_KEY")

# How long an access token lasts, in minutes
ACCESS_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Secret that signs refresh tokens, different from the access secret
REFRESH_SECRET = os.getenv("REFRESH_TOKEN_SECRET_KEY")

# How long a refresh token lasts, in days
REFRESH_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Longest a session can last since the first login, in days
SESSION_MAX_DAYS = int(os.getenv("SESSION_MAX_DAYS", "7"))

# Frontend addresses allowed to call the API, comma separated in .env
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",") if origin.strip()]

# Address of json-server, our database
DB_URL = os.getenv("DB_URL", "http://localhost:4000")

# Send the cookie over HTTPS only, keep false on localhost
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"

# Max login and register attempts, for example 5/minute
AUTH_RATE_LIMIT = os.getenv("AUTH_RATE_LIMIT", "5/minute")

# Seconds a replaced session keeps working, so two tabs refreshing at once do not break each other
REFRESH_GRACE_SECONDS = int(os.getenv("REFRESH_GRACE_SECONDS", "10"))

# One shared HTTP client used for every database call
db = httpx.Client(base_url=DB_URL)
