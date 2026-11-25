from pydantic import BaseModel, Field


# Sign up rules
class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=6, max_length=128)


# User without password
class User(BaseModel):
    id: int
    username: str
    role: str = "client"


# Login response
class AuthResponse(BaseModel):
    access_token: str
    user: User


# New todo
class TodoCreate(BaseModel):
    title: str


# Tick todo
class TodoUpdate(BaseModel):
    done: bool
