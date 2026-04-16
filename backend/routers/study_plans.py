import json
import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PROGRESS_DIR = os.path.join(DATA_DIR, "progress")


def load_plans() -> list[dict]:
    path = os.path.join(DATA_DIR, "study_plans.json")
    with open(path) as f:
        return json.load(f)


def load_progress(user_id: str, plan_id: str) -> dict:
    os.makedirs(PROGRESS_DIR, exist_ok=True)
    path = os.path.join(PROGRESS_DIR, f"{user_id}_{plan_id}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"user_id": user_id, "plan_id": plan_id, "completed": []}


def save_progress(user_id: str, plan_id: str, progress: dict):
    os.makedirs(PROGRESS_DIR, exist_ok=True)
    path = os.path.join(PROGRESS_DIR, f"{user_id}_{plan_id}.json")
    with open(path, "w") as f:
        json.dump(progress, f, indent=2)


@router.get("/plans")
def get_plans():
    """Return all available study plans (metadata only, no full question lists)."""
    plans = load_plans()
    return [{
        "id": p["id"],
        "title": p["title"],
        "description": p["description"],
        "duration_weeks": p["duration_weeks"],
        "questions_per_day": p["questions_per_day"],
        "total_questions": sum(
            len(day["question_ids"])
            for week in p["weeks"]
            for day in week["days"]
        ),
    } for p in plans]


@router.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    """Return full plan with weekly schedule."""
    plans = load_plans()
    for p in plans:
        if p["id"] == plan_id:
            return p
    return {"error": "Plan not found"}


@router.get("/plans/{plan_id}/progress")
def get_progress(plan_id: str, user_id: Optional[str] = "default"):
    """Get user's progress on a plan."""
    return load_progress(user_id, plan_id)


class MarkCompleteRequest(BaseModel):
    user_id: str = "default"
    question_id: str


@router.post("/plans/{plan_id}/complete")
def mark_complete(plan_id: str, req: MarkCompleteRequest):
    """Mark a question as completed in a study plan."""
    progress = load_progress(req.user_id, plan_id)
    if req.question_id not in progress["completed"]:
        progress["completed"].append(req.question_id)
    save_progress(req.user_id, plan_id, progress)
    return progress
