import uuid
from datetime import datetime, timedelta, timezone

import httpx
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.config import (
    ACCESS_MINUTES,
    ACCESS_SECRET,
    ALGORITHM,
    REFRESH_DAYS,
    REFRESH_GRACE_SECONDS,
    REFRESH_SECRET,
    SESSION_MAX_DAYS,
    db,
)
from app.models import User

# Password hashing and token reader
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Access token
def create_access_token(user_id: int, sid: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "sid": sid, "type": "access", "exp": exp},
        ACCESS_SECRET,
        algorithm=ALGORITHM,
    )

# Refresh token
def create_refresh_token(
    user_id: int, session_start: datetime | None = None
) -> tuple[str, str, datetime]:
    now = datetime.now(timezone.utc)
    session_start = session_start or now
    exp = min(
        now + timedelta(days=REFRESH_DAYS),
        session_start + timedelta(days=SESSION_MAX_DAYS),
    )
    # New session ID
    jti = uuid.uuid4().hex
    token = jwt.encode(
        {
            "sub": str(user_id),
            "jti": jti,
            "type": "refresh",
            "start": int(session_start.timestamp()),
            "exp": exp,
        },
        REFRESH_SECRET,
        algorithm=ALGORITHM,
    )
    return token, jti, exp

# Check session is active
def get_live_session(session_id: str) -> dict | None:
    res = db.get(f"/refresh_tokens/{session_id}")
    if res.status_code != 200:
        return None
    session = res.json()
    replaced_at = session.get("replaced_at")
    if replaced_at is not None:
        age = datetime.now(timezone.utc) - datetime.fromisoformat(replaced_at)
        if age.total_seconds() > REFRESH_GRACE_SECONDS:
            return None
    return session

# Get logged in user
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, ACCESS_SECRET, algorithms=[ALGORITHM])
        if payload["type"] != "access":
            raise ValueError
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
