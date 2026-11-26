from pydantic import BaseModel, ConfigDict, Field


# rules
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


# todo title check
class TodoCreate(BaseModel):
    # Trim spaces
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=100)


# Tick todo
class TodoUpdate(BaseModel):
    done: bool
