from fastapi import HTTPException

from app.models import TodoCreate, TodoUpdate, User
from app.utils.db import database


# Check todo ownership
def own_todo(todo_id: int, user: User) -> dict:
    db_response = database.get(f"/todos/{todo_id}")
    if db_response.status_code != 200 or db_response.json()["user_id"] != user.id:
        raise HTTPException(404, "Todo not found")
    return db_response.json()


# List todos
def list_todos(user: User) -> list:
    return database.get("/todos", params={"user_id": user.id}).json()


# Add todo
def create_todo(todo_data: TodoCreate, user: User) -> dict:
    todo = {"user_id": user.id, "title": todo_data.title, "done": False}
    return database.post("/todos", json=todo).json()


# Update todo
def update_todo(todo_id: int, todo_data: TodoUpdate, user: User) -> dict:
    own_todo(todo_id, user)
    return database.patch(f"/todos/{todo_id}", json={"done": todo_data.done}).json()


# Delete todo
def delete_todo(todo_id: int, user: User) -> None:
    own_todo(todo_id, user)
    database.delete(f"/todos/{todo_id}")
