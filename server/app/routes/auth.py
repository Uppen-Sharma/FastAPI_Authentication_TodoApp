from datetime import datetime, timezone
import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.config import ALGORITHM, AUTH_RATE_LIMIT, COOKIE_SECURE, REFRESH_GRACE_SECONDS, REFRESH_SECRET, db
from app.limiter import limiter
from app.models import AuthResponse, RegisterRequest, User
from app.security import create_access_token, create_refresh_token, get_live_session, password_hash

router = APIRouter(prefix="/auth", tags=["auth"])

# Issue new access token using the user ID and Session ID if it exists and is valid
def issue_tokens(user: dict, response: Response, session_start: datetime | None = None) -> AuthResponse:
    refresh, jti, exp = create_refresh_token(user["id"], session_start)
    db.post("/refresh_tokens", json={"id": jti, "user_id": user["id"], "exp": exp.isoformat()})
    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=int((exp - datetime.now(timezone.utc)).total_seconds()),
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/auth",
    )
    # Return the access token and user information in the response
    return AuthResponse(
        access_token=create_access_token(user["id"], jti),
        user=User(id=user["id"], username=user["username"], role=user.get("role", "client")),
    )

# Delete a user's expired sessions and sessions replaced longer ago than the grace period, runs on login and refresh
def delete_expired_sessions(user_id: int) -> None:
    now = datetime.now(timezone.utc)
    sessions = db.get("/refresh_tokens", params={"user_id": user_id}).json()
    for session in sessions:
        expired = datetime.fromisoformat(session["exp"]) < now
        replaced_at = session.get("replaced_at")
        replaced_too_long_ago = (
            replaced_at is not None
            and (now - datetime.fromisoformat(replaced_at)).total_seconds() > REFRESH_GRACE_SECONDS
        )
        if expired or replaced_too_long_ago:
            db.delete(f"/refresh_tokens/{session['id']}")

# Register a new user with a unique username and hashed password
@router.post("/register", response_model=User, status_code=201)
@limiter.limit(AUTH_RATE_LIMIT)
def register(request: Request, data: RegisterRequest):
    username = data.username.strip().lower()
    if db.get("/users", params={"username": username}).json():
        raise HTTPException(409, "Username already taken")
    user = db.post(
        "/users",
        json={"username": username, "password_hash": password_hash.hash(data.password), "role": "client"},
    ).json()
    return User(id=user["id"], username=user["username"], role=user["role"])

# Login a user with a valid username and password, issue new access and refresh tokens
@router.post("/login", response_model=AuthResponse)
@limiter.limit(AUTH_RATE_LIMIT)
def login(request: Request, response: Response, form: OAuth2PasswordRequestForm = Depends()):
    users = db.get("/users", params={"username": form.username.strip().lower()}).json()
    if not users or not password_hash.verify(form.password, users[0]["password_hash"]):
        raise HTTPException(401, "Wrong username or password")
    delete_expired_sessions(users[0]["id"])
    return issue_tokens(users[0], response)

# restoreSession() triggers this to issue new tokens if the refresh token is valid, returns nothing without a cookie and a 401 if it is invalid or expired
@router.post("/refresh", response_model=AuthResponse | None)
def refresh(response: Response, refresh_token: str | None = Cookie(default=None)):
    if refresh_token is None:
        return None
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=[ALGORITHM])
        if payload["type"] != "refresh":
            raise ValueError
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(401, "Session expired")


    session = get_live_session(payload["jti"])
    if session is None:
        db.delete(f"/refresh_tokens/{payload['jti']}")
        raise HTTPException(401, "Session expired")
    # Do not delete the old session yet, mark it as replaced so it stops working after the grace period
    if session.get("replaced_at") is None:
        db.patch(
            f"/refresh_tokens/{payload['jti']}",
            json={"replaced_at": datetime.now(timezone.utc).isoformat()},
        )

    user = db.get(f"/users/{payload['sub']}").json()
    delete_expired_sessions(user["id"])
    session_start = datetime.fromtimestamp(payload["start"], timezone.utc)
    return issue_tokens(user, response, session_start)

# Logout endpoint to delete the refresh token from the database and clear the cookie
@router.post("/logout", status_code=204)
def logout(response: Response, refresh_token: str | None = Cookie(default=None)):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=[ALGORITHM])
        db.delete(f"/refresh_tokens/{payload['jti']}")
    except (jwt.PyJWTError, KeyError):
        pass
    response.delete_cookie("refresh_token", path="/auth")
