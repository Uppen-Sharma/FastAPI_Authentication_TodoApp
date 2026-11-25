from fastapi import FastAPI

from app.middleware.cors import add_cors
from app.middleware.rate_limit import add_rate_limit
from app.routes import admin, auth, client

# Application instance
app = FastAPI()

# Middleware
add_rate_limit(app)
add_cors(app)

# Routes
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(admin.router)
