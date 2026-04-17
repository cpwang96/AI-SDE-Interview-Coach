"""Per-question personal notes and "needs review" flags."""
import json
import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

NOTES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notes")
FLAGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "flags")


# ── Notes helpers ─────────────────────────────────────────────────────────────

def _load_notes(user_id: str) -> dict:
    os.makedirs(NOTES_DIR, exist_ok=True)
    path = os.path.join(NOTES_DIR, f"{user_id}.json")
    return json.load(open(path)) if os.path.exists(path) else {}


def _save_notes(user_id: str, notes: dict):
    os.makedirs(NOTES_DIR, exist_ok=True)
    with open(os.path.join(NOTES_DIR, f"{user_id}.json"), "w") as f:
        json.dump(notes, f, indent=2)


# ── Flags helpers ─────────────────────────────────────────────────────────────

def _load_flags(user_id: str) -> list:
    os.makedirs(FLAGS_DIR, exist_ok=True)
    path = os.path.join(FLAGS_DIR, f"{user_id}.json")
    return json.load(open(path)) if os.path.exists(path) else []


def _save_flags(user_id: str, flags: list):
    os.makedirs(FLAGS_DIR, exist_ok=True)
    with open(os.path.join(FLAGS_DIR, f"{user_id}.json"), "w") as f:
        json.dump(flags, f, indent=2)


# ── Routes — flags first so /flags isn't swallowed by /{question_id} ─────────

@router.get("/flags")
def get_all_flags(user_id: str = "default"):
    """Return list of all flagged question IDs for a user."""
    return _load_flags(user_id)


@router.post("/{question_id}/flag")
def toggle_flag(question_id: str, user_id: str = "default"):
    """Toggle the 'needs review' flag for a question. Returns new state."""
    flags = _load_flags(user_id)
    if question_id in flags:
        flags.remove(question_id)
        flagged = False
    else:
        flags.append(question_id)
        flagged = True
    _save_flags(user_id, flags)
    return {"flagged": flagged}


# ── Routes — notes ────────────────────────────────────────────────────────────

@router.get("/{question_id}")
def get_note(question_id: str, user_id: str = "default"):
    notes = _load_notes(user_id)
    flags = _load_flags(user_id)
    return {"note": notes.get(question_id, ""), "flagged": question_id in flags}


class SaveNoteRequest(BaseModel):
    user_id: str = "default"
    note: str


@router.post("/{question_id}")
def save_note(question_id: str, req: SaveNoteRequest):
    notes = _load_notes(req.user_id)
    if req.note.strip():
        notes[question_id] = req.note
    elif question_id in notes:
        del notes[question_id]
    _save_notes(req.user_id, notes)
    return {"ok": True}
