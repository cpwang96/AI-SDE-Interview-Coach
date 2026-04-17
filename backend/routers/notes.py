"""Per-question personal notes, stored as a single JSON file per user."""
import json
import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notes")


def _load(user_id: str) -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def _save(user_id: str, notes: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{user_id}.json")
    with open(path, "w") as f:
        json.dump(notes, f, indent=2)


@router.get("/{question_id}")
def get_note(question_id: str, user_id: str = "default"):
    notes = _load(user_id)
    return {"note": notes.get(question_id, "")}


class SaveNoteRequest(BaseModel):
    user_id: str = "default"
    note: str


@router.post("/{question_id}")
def save_note(question_id: str, req: SaveNoteRequest):
    notes = _load(req.user_id)
    if req.note.strip():
        notes[question_id] = req.note
    elif question_id in notes:
        del notes[question_id]  # clear empty notes instead of storing ""
    _save(req.user_id, notes)
    return {"ok": True}
