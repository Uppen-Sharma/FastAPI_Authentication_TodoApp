from fastapi import APIRouter, Depends, HTTPException
from app.config import db
from app.models import TodoCreate, TodoUpdate, User
from app.security import require_role

# Only users with the admin role may call these routes
require_admin = require_role("admin")

# Routes for admins: they work with every user's todos, other roles get a 403
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)


# Check that a todo exists, any owner is fine for an admin
def find_todo(todo_id: int) -> dict:
    res = db.get(f"/todos/{todo_id}")
    if res.status_code != 200:
        raise HTTPException(404, "Todo not found")
    return res.json()


# List every user's todos, each with the username of its owner
@router.get("/todos")
def all_todos():
    usernames = {u["id"]: u["username"] for u in db.get("/users").json()}
    return [
        {**todo, "owner": usernames.get(todo["user_id"], "unknown")}
        for todo in db.get("/todos").json()
    ]


# Create a new todo for the admin
@router.post("/todos", status_code=201)
def create_todo(data: TodoCreate, user: User = Depends(require_admin)):
    todo = {"user_id": user.id, "title": data.title, "done": False}
    return db.post("/todos", json=todo).json()


# Tick or untick a todo that belongs to any user
@router.put("/todos/{todo_id}")
def update_any_todo(todo_id: int, data: TodoUpdate):
    find_todo(todo_id)
    return db.patch(f"/todos/{todo_id}", json={"done": data.done}).json()


# Delete a todo that belongs to any user
@router.delete("/todos/{todo_id}", status_code=204)
def delete_any_todo(todo_id: int):
    find_todo(todo_id)
    db.delete(f"/todos/{todo_id}")
