from fastapi import HTTPException

from app.models import TodoCreate, TodoUpdate, User
from app.utils.db import db


# Check todo ownership
def own_todo(todo_id: int, user: User) -> dict:
    res = db.get(f"/todos/{todo_id}")
    if res.status_code != 200 or res.json()["user_id"] != user.id:
        raise HTTPException(404, "Todo not found")
    return res.json()


# List todos
def list_todos(user: User) -> list:
    return db.get("/todos", params={"user_id": user.id}).json()


# Add todo
def create_todo(data: TodoCreate, user: User) -> dict:
    todo = {"user_id": user.id, "title": data.title, "done": False}
    return db.post("/todos", json=todo).json()


# Update todo
def update_todo(todo_id: int, data: TodoUpdate, user: User) -> dict:
    own_todo(todo_id, user)
    return db.patch(f"/todos/{todo_id}", json={"done": data.done}).json()


# Delete todo
def delete_todo(todo_id: int, user: User) -> None:
    own_todo(todo_id, user)
    db.delete(f"/todos/{todo_id}")
