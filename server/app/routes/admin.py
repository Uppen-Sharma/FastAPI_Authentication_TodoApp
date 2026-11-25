from fastapi import APIRouter, Depends, HTTPException
from app.config import db
from app.models import TodoCreate, TodoUpdate, User
from app.security import require_role

# Admins only
require_admin = require_role("admin")

# Admin routes
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)


# Check todo exists
def find_todo(todo_id: int) -> dict:
    res = db.get(f"/todos/{todo_id}")
    if res.status_code != 200:
        raise HTTPException(404, "Todo not found")
    return res.json()


# All todos with owners
@router.get("/todos")
def all_todos():
    usernames = {u["id"]: u["username"] for u in db.get("/users").json()}
    return [
        {**todo, "owner": usernames.get(todo["user_id"], "unknown")}
        for todo in db.get("/todos").json()
    ]


# Add todo
@router.post("/todos", status_code=201)
def create_todo(data: TodoCreate, user: User = Depends(require_admin)):
    todo = {"user_id": user.id, "title": data.title, "done": False}
    return db.post("/todos", json=todo).json()


# Update any todo
@router.put("/todos/{todo_id}")
def update_any_todo(todo_id: int, data: TodoUpdate):
    find_todo(todo_id)
    return db.patch(f"/todos/{todo_id}", json={"done": data.done}).json()


# Delete any todo
@router.delete("/todos/{todo_id}", status_code=204)
def delete_any_todo(todo_id: int):
    find_todo(todo_id)
    db.delete(f"/todos/{todo_id}")
