import json
import os
from datetime import date
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


def _flatten_days(plan: dict) -> list[dict]:
    """Return all days in order, each annotated with week_num and theme."""
    result = []
    for week in plan["weeks"]:
        for day in week["days"]:
            result.append({**day, "week_num": week["week"], "theme": week["theme"]})
    return result


def compute_plan_stats(plan: dict, progress: dict) -> dict:
    """Attach computed fields (today's day, streak, on-track status) to a progress dict."""
    completed_set = set(progress.get("completed", []))
    all_days = _flatten_days(plan)
    started_at = progress.get("started_at")

    if not started_at:
        return {
            **progress,
            "started": False,
            "current_day_num": 0,
            "current_week_num": 1,
            "today_day": None,
            "today_question_ids": [],
            "past_incomplete_count": 0,
            "days_elapsed": 0,
            "total_plan_days": len(all_days),
            "plan_finished": False,
        }

    today = date.today()
    started = date.fromisoformat(started_at)
    days_elapsed = (today - started).days  # 0 = plan day 1

    plan_finished = days_elapsed >= len(all_days)
    today_idx = min(days_elapsed, len(all_days) - 1)
    today_day = all_days[today_idx]
    today_question_ids = today_day["question_ids"] if not plan_finished else []

    # Questions from past days (before today) that aren't done
    past_incomplete = sum(
        1
        for i, d in enumerate(all_days)
        if i < days_elapsed
        for qid in d["question_ids"]
        if qid not in completed_set
    )

    return {
        **progress,
        "started": True,
        "current_day_num": days_elapsed + 1,
        "current_week_num": today_day["week_num"],
        "today_day": today_day,
        "today_question_ids": today_question_ids,
        "past_incomplete_count": past_incomplete,
        "days_elapsed": days_elapsed,
        "total_plan_days": len(all_days),
        "plan_finished": plan_finished,
    }


@router.get("/plans")
def get_plans():
    """Return all available study plans (metadata only)."""
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
    """Get user's progress on a plan, with computed stats."""
    plans = load_plans()
    plan = next((p for p in plans if p["id"] == plan_id), None)
    progress = load_progress(user_id, plan_id)
    if plan:
        return compute_plan_stats(plan, progress)
    return progress


class StartPlanRequest(BaseModel):
    user_id: str = "default"


@router.post("/plans/{plan_id}/start")
def start_plan(plan_id: str, req: StartPlanRequest):
    """Record the start date for a plan (idempotent — won't overwrite if already started)."""
    progress = load_progress(req.user_id, plan_id)
    if "started_at" not in progress:
        progress["started_at"] = date.today().isoformat()
        progress.setdefault("streak", 0)
        progress.setdefault("last_activity_date", None)
        save_progress(req.user_id, plan_id, progress)

    plans = load_plans()
    plan = next((p for p in plans if p["id"] == plan_id), None)
    if plan:
        return compute_plan_stats(plan, progress)
    return progress


class MarkCompleteRequest(BaseModel):
    user_id: str = "default"
    question_id: str


@router.post("/plans/{plan_id}/complete")
def mark_complete(plan_id: str, req: MarkCompleteRequest):
    """Toggle a question's completion status. Streak only advances on marking done."""
    progress = load_progress(req.user_id, plan_id)

    toggling_off = req.question_id in progress["completed"]
    if toggling_off:
        progress["completed"].remove(req.question_id)
    else:
        progress["completed"].append(req.question_id)

    # Update streak only when marking done (not when unmarking)
    if not toggling_off:
        today_str = date.today().isoformat()
        last = progress.get("last_activity_date")
        if last != today_str:
            if last:
                gap = (date.today() - date.fromisoformat(last)).days
                if gap == 1:
                    progress["streak"] = progress.get("streak", 0) + 1
                else:
                    progress["streak"] = 1  # streak broken, restart
            else:
                progress["streak"] = 1  # first activity ever
            progress["last_activity_date"] = today_str

    save_progress(req.user_id, plan_id, progress)

    plans = load_plans()
    plan = next((p for p in plans if p["id"] == plan_id), None)
    if plan:
        return compute_plan_stats(plan, progress)
    return progress
