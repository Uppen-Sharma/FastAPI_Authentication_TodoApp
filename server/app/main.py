from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.config import CORS_ORIGINS
from app.limiter import limiter
from app.routes import admin, auth, client

# The FastAPI application
app = FastAPI()

# Make the rate limiter available to the routes
app.state.limiter = limiter


# Reply with a 429 when someone goes over the rate limit
@app.exception_handler(RateLimitExceeded)
async def rate_limited(request, exc):
    return JSONResponse({"detail": "Too many attempts, try again in a minute"}, status_code=429)

# Only the listed frontend addresses may call the API, and the cookie is allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Attach the route files
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(admin.router)
