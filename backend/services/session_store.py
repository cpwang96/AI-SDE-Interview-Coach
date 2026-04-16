import json
import os
from datetime import datetime, timezone
from typing import Optional
from models.schemas import SavedSession

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sessions")


def _user_dir(user_id: str) -> str:
    d = os.path.join(DATA_DIR, user_id)
    os.makedirs(d, exist_ok=True)
    return d


def save_session(session: SavedSession) -> None:
    d = _user_dir(session.user_id)
    date = session.started_at[:10]  # YYYY-MM-DD
    q = session.question_id or session.session_type
    fname = f"{date}_{q}_{session.session_id[:8]}.json"
    with open(os.path.join(d, fname), "w") as f:
        json.dump(session.model_dump(), f, indent=2)


def get_user_sessions(user_id: str) -> list[SavedSession]:
    d = _user_dir(user_id)
    sessions = []
    for fname in sorted(os.listdir(d)):
        if fname.endswith(".json"):
            with open(os.path.join(d, fname)) as f:
                sessions.append(SavedSession(**json.load(f)))
    return sessions


def get_session(user_id: str, session_id: str) -> Optional[SavedSession]:
    d = _user_dir(user_id)
    for fname in os.listdir(d):
        if session_id[:8] in fname:
            with open(os.path.join(d, fname)) as f:
                return SavedSession(**json.load(f))
    return None
