from fastapi import APIRouter, Depends, HTTPException
from app.config import db
from app.models import TodoCreate, TodoUpdate, User
from app.security import require_role

# Routes for clients: each client manages only their own todos, other roles get a 403
router = APIRouter(prefix="/client", tags=["client"])

# Only users with the client role may call these routes
require_client = require_role("client")


# Find a todo by id, but only if it belongs to the user
def own_todo(todo_id: int, user: User) -> dict:
    res = db.get(f"/todos/{todo_id}")
    if res.status_code != 200 or res.json()["user_id"] != user.id:
        raise HTTPException(404, "Todo not found")
    return res.json()


# List the client's own todos
@router.get("/todos")
def list_todos(user: User = Depends(require_client)):
    return db.get("/todos", params={"user_id": user.id}).json()


# Create a new todo for the client
@router.post("/todos", status_code=201)
def create_todo(data: TodoCreate, user: User = Depends(require_client)):
    todo = {"user_id": user.id, "title": data.title, "done": False}
    return db.post("/todos", json=todo).json()


# Tick or untick one of the client's own todos
@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate, user: User = Depends(require_client)):
    own_todo(todo_id, user)
    return db.patch(f"/todos/{todo_id}", json={"done": data.done}).json()


# Delete one of the client's own todos
@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, user: User = Depends(require_client)):
    own_todo(todo_id, user)
    db.delete(f"/todos/{todo_id}")
