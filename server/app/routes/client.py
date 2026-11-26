from fastapi import APIRouter, Depends

from app.controllers import client_controller
from app.middleware.auth import require_client
from app.models import TodoCreate, TodoUpdate, User

# Client routes
router = APIRouter(
    prefix="/client",
    tags=["client"],
    dependencies=[Depends(require_client)],
)


# List todos
@router.get("/todos")
def list_todos(user: User = Depends(require_client)):
    return client_controller.list_todos(user)


# Add todo
@router.post("/todos", status_code=201)
def create_todo(todo_data: TodoCreate, user: User = Depends(require_client)):
    return client_controller.create_todo(todo_data, user)


# Update todo
@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo_data: TodoUpdate, user: User = Depends(require_client)):
    return client_controller.update_todo(todo_id, todo_data, user)


# Delete todo
@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, user: User = Depends(require_client)):
    client_controller.delete_todo(todo_id, user)
