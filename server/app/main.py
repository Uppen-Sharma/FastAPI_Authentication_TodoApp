from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.config import CORS_ORIGINS
from app.limiter import limiter
from app.routes import admin, auth, client

# App
app = FastAPI()

# Rate limiter
app.state.limiter = limiter


# Too many requests
@app.exception_handler(RateLimitExceeded)
async def rate_limited(request, exc):
    return JSONResponse({"detail": "Too many attempts, try again in a minute"}, status_code=429)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Routes
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(admin.router)
