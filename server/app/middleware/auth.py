import httpx
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import ACCESS_SECRET
from app.models import User
from app.utils.db import db
from app.utils.sessions import get_live_session
from app.utils.tokens import decode_token

# Token reader/swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Get logged in user
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_token(token, ACCESS_SECRET, "access")
        if get_live_session(payload["sid"]) is None:
            raise ValueError
        res = db.get(f"/users/{payload['sub']}")
        res.raise_for_status()
    except (jwt.PyJWTError, KeyError, ValueError, httpx.HTTPError):
        raise HTTPException(401, "Invalid or expired token")
    return User(**res.json())  # Drops password hash


# Check user role
def require_role(*roles: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "Restricted route")
        return user

    return checker


# Role guards
require_admin = require_role("admin")
require_client = require_role("client")
