from fastapi import APIRouter, Depends, HTTPException
from app.config import db
from app.models import TodoCreate, TodoUpdate, User
from app.security import require_role

# Client routes
router = APIRouter(prefix="/client", tags=["client"])

# Clients only
require_client = require_role("client")


# Check todo ownership
def own_todo(todo_id: int, user: User) -> dict:
    res = db.get(f"/todos/{todo_id}")
    if res.status_code != 200 or res.json()["user_id"] != user.id:
        raise HTTPException(404, "Todo not found")
    return res.json()


# List todos
@router.get("/todos")
def list_todos(user: User = Depends(require_client)):
    return db.get("/todos", params={"user_id": user.id}).json()


# Add todo
@router.post("/todos", status_code=201)
def create_todo(data: TodoCreate, user: User = Depends(require_client)):
    todo = {"user_id": user.id, "title": data.title, "done": False}
    return db.post("/todos", json=todo).json()


# Update todo
@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate, user: User = Depends(require_client)):
    own_todo(todo_id, user)
    return db.patch(f"/todos/{todo_id}", json={"done": data.done}).json()


# Delete todo
@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, user: User = Depends(require_client)):
    own_todo(todo_id, user)
    db.delete(f"/todos/{todo_id}")
