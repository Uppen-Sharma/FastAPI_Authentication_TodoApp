from fastapi import APIRouter, Cookie, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.config import AUTH_RATE_LIMIT
from app.controllers import auth_controller
from app.middleware.rate_limit import limiter
from app.models import AuthResponse, RegisterRequest, User

# Auth routes
router = APIRouter(prefix="/auth", tags=["auth"])


# Register
@router.post("/register", response_model=User, status_code=201)
@limiter.limit(AUTH_RATE_LIMIT)
def register(request: Request, register_data: RegisterRequest):
    return auth_controller.register_user(register_data)


# Login
@router.post("/login", response_model=AuthResponse)
@limiter.limit(AUTH_RATE_LIMIT)
def login(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_controller.login_user(form_data.username, form_data.password, response)


# Refresh tokens
@router.post("/refresh", response_model=AuthResponse | None)
def refresh(response: Response, refresh_token: str | None = Cookie(default=None)):
    return auth_controller.refresh_session(refresh_token, response)


# Logout
@router.post("/logout", status_code=204)
def logout(response: Response, refresh_token: str | None = Cookie(default=None)):
    auth_controller.logout_user(refresh_token, response)
