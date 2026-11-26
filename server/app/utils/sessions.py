from datetime import datetime, timezone

from app.config import REFRESH_GRACE_SECONDS
from app.utils.db import db


# Long time since session was replaced
# make sure that session was in grace but not for too long 
def is_stale(session: dict) -> bool:
    replaced_at = session.get("replaced_at")
    if replaced_at is None:
        return False
    age = datetime.now(timezone.utc) - datetime.fromisoformat(replaced_at)
    return age.total_seconds() > REFRESH_GRACE_SECONDS


# Check session is active
def get_live_session(session_id: str) -> dict | None:
    res = db.get(f"/refresh_tokens/{session_id}")
    if res.status_code != 200:
        return None
    session = res.json()
    return None if is_stale(session) else session


# Remove dead sessions
def delete_expired_sessions(user_id: int) -> None:
    now = datetime.now(timezone.utc)
    sessions = db.get("/refresh_tokens", params={"user_id": user_id}).json()
    for session in sessions:
        expired = datetime.fromisoformat(session["exp"]) < now
        if expired or is_stale(session):
            db.delete(f"/refresh_tokens/{session['id']}")
