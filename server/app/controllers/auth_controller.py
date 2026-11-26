from datetime import datetime, timezone

import jwt
from fastapi import HTTPException, Response

from app.config import COOKIE_SECURE, REFRESH_SECRET
from app.models import AuthResponse, RegisterRequest, User
from app.utils.db import database
from app.utils.password import password_hash
from app.utils.sessions import delete_expired_sessions, get_live_session
from app.utils.tokens import create_access_token, create_refresh_token, decode_token


# Issue both tokens
def issue_tokens(user: dict, response: Response, session_start: datetime | None = None) -> AuthResponse:
    new_refresh_token, jwt_id, expiry = create_refresh_token(user["id"], session_start)
    database.post("/refresh_tokens", json={"id": jwt_id, "user_id": user["id"], "expiry": expiry.isoformat()})
    response.set_cookie(
        "refresh_token",
        new_refresh_token,
        max_age=int((expiry - datetime.now(timezone.utc)).total_seconds()),
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/auth",
    )
    # Return access token and user
    return AuthResponse(
        access_token=create_access_token(user["id"], jwt_id),
        user=User(id=user["id"], username=user["username"], role=user.get("role", "client")),
    )


# Register new user
def register_user(register_data: RegisterRequest) -> User:
    username = register_data.username.strip().lower()
    if database.get("/users", params={"username": username}).json():
        raise HTTPException(409, "Username already taken")
    user = database.post(
        "/users",
        json={"username": username, "password_hash": password_hash.hash(register_data.password), "role": "client"},
    ).json()
    return User(id=user["id"], username=user["username"], role=user["role"])


# Login user
def login_user(username: str, password: str, response: Response) -> AuthResponse:
    users = database.get("/users", params={"username": username.strip().lower()}).json()
    if not users or not password_hash.verify(password, users[0]["password_hash"]):
        raise HTTPException(401, "Wrong username or password")
    delete_expired_sessions(users[0]["id"])
    return issue_tokens(users[0], response)


# Refresh tokens
def refresh_session(refresh_token: str | None, response: Response) -> AuthResponse | None:
    if refresh_token is None:
        return None
    try:
        payload = decode_token(refresh_token, REFRESH_SECRET, "refresh")
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(401, "Session expired")

    session = get_live_session(payload["jti"])
    if session is None:
        database.delete(f"/refresh_tokens/{payload['jti']}")
        raise HTTPException(401, "Session expired")
    # Keep old session for a short time
    if session.get("replaced_at") is None:
        database.patch(
            f"/refresh_tokens/{payload['jti']}",
            json={"replaced_at": datetime.now(timezone.utc).isoformat()},
        )

    user = database.get(f"/users/{payload['sub']}").json()
    delete_expired_sessions(user["id"])
    session_start = datetime.fromtimestamp(payload["start"], timezone.utc)
    return issue_tokens(user, response, session_start)


# Logout
def logout_user(refresh_token: str | None, response: Response) -> None:
    if refresh_token is not None:
        try:
            payload = decode_token(refresh_token, REFRESH_SECRET, "refresh")
            database.delete(f"/refresh_tokens/{payload['jti']}")
        except (jwt.PyJWTError, KeyError, ValueError):
            pass
    response.delete_cookie("refresh_token", path="/auth")
