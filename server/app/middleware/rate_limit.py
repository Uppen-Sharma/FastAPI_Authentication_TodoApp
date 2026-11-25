from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Rate limit per IP
limiter = Limiter(key_func=get_remote_address)


# Rate limit exceeded handler
async def rate_limited(request: Request, exc: Exception):
    return JSONResponse({"detail": "Too many attempts, try again in a minute"}, status_code=429)


# Rate limiter
def add_rate_limit(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limited)
