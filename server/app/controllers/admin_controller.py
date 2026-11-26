from fastapi import HTTPException

from app.utils.db import database


# Check todo exists
def find_todo(todo_id: int) -> dict:
    db_response = database.get(f"/todos/{todo_id}")
    if db_response.status_code != 200:
        raise HTTPException(404, "Todo not found")
    return db_response.json()


# All todos with owners
def all_todos() -> list:
    
    usernames = {user["id"]: user["username"] for user in database.get("/users").json()}
    return [
        {**todo, "owner": usernames.get(todo["user_id"], "unknown")}
        for todo in database.get("/todos").json()
    ]


# Delete any todo
def delete_any_todo(todo_id: int) -> None:
    find_todo(todo_id)
    database.delete(f"/todos/{todo_id}")
