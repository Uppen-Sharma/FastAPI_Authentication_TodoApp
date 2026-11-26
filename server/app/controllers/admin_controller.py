from fastapi import HTTPException

from app.utils.db import db


# Check todo exists
def find_todo(todo_id: int) -> dict:
    res = db.get(f"/todos/{todo_id}")
    if res.status_code != 200:
        raise HTTPException(404, "Todo not found")
    return res.json()


# All todos with owners
def all_todos() -> list:
    usernames = {u["id"]: u["username"] for u in db.get("/users").json()}
    return [
        {**todo, "owner": usernames.get(todo["user_id"], "unknown")}
        for todo in db.get("/todos").json()
    ]


# Delete any todo
def delete_any_todo(todo_id: int) -> None:
    find_todo(todo_id)
    db.delete(f"/todos/{todo_id}")
