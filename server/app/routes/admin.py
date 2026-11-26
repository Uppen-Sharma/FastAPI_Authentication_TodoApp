from fastapi import APIRouter, Depends

from app.controllers import admin_controller, client_controller
from app.middleware.auth import require_admin
from app.models import TodoCreate, TodoUpdate, User

# Admin routes
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)


# All todos with owners
@router.get("/todos")
def all_todos():
    return admin_controller.all_todos()


# Add own todo
@router.post("/todos", status_code=201)
def create_todo(data: TodoCreate, user: User = Depends(require_admin)):
    return client_controller.create_todo(data, user)


# Update own todo only
@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate, user: User = Depends(require_admin)):
    return client_controller.update_todo(todo_id, data, user)


# Delete any todo
@router.delete("/todos/{todo_id}", status_code=204)
def delete_any_todo(todo_id: int):
    admin_controller.delete_any_todo(todo_id)
