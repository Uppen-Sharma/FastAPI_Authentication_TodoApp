import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.config import (
    ACCESS_MINUTES,
    ACCESS_SECRET,
    ALGORITHM,
    REFRESH_DAYS,
    REFRESH_SECRET,
    SESSION_MAX_DAYS,
)


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


# Verify token and type
def decode_token(token: str, secret: str, token_type: str) -> dict:
    payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    if payload["type"] != token_type:
        raise ValueError
    return payload
