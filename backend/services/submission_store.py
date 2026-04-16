"""Simple JSON-file store for submission history."""
import json
import os
from datetime import datetime
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "submissions")


def _path(user_id: str) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, f"{user_id}.json")


def load_submissions(user_id: str) -> list[dict]:
    p = _path(user_id)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return []


def save_submission(
    user_id: str,
    question_id: str,
    code: str,
    language: str,
    passed: int,
    total: int,
    all_passed: bool,
) -> dict:
    subs = load_submissions(user_id)
    entry = {
        "question_id": question_id,
        "code": code,
        "language": language,
        "passed": passed,
        "total": total,
        "all_passed": all_passed,
        "submitted_at": datetime.now().isoformat(),
    }
    subs.append(entry)
    with open(_path(user_id), "w") as f:
        json.dump(subs, f, indent=2)
    return entry


def get_solved_questions(user_id: str) -> list[str]:
    """Return list of question_ids that the user has solved (all tests passed)."""
    subs = load_submissions(user_id)
    return list({s["question_id"] for s in subs if s.get("all_passed")})


def get_latest_submission(user_id: str, question_id: str) -> Optional[dict]:
    """Return the most recent submission for a question."""
    subs = load_submissions(user_id)
    matches = [s for s in subs if s["question_id"] == question_id]
    return matches[-1] if matches else None
