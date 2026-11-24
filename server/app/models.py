from pydantic import BaseModel, Field


# Data the sign up form sends, with the rules for each field
class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=6, max_length=128)


# A user as the app sees it, never includes the password hash
class User(BaseModel):
    id: int
    username: str
    role: str = "client"


# What login and refresh send back: the access token and the user
class AuthResponse(BaseModel):
    access_token: str
    user: User


# Data needed to create a todo
class TodoCreate(BaseModel):
    title: str


# Data needed to tick or untick a todo
class TodoUpdate(BaseModel):
    done: bool
