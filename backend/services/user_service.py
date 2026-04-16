import json
import os
from datetime import datetime, timezone
from typing import Optional
from models.schemas import UserProfile, CreateProfileRequest

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users")


def _user_path(user_id: str) -> str:
    return os.path.join(DATA_DIR, f"{user_id}.json")


def create_profile(user_id: str, req: CreateProfileRequest) -> UserProfile:
    now = datetime.now(timezone.utc).isoformat()
    profile = UserProfile(
        user_id=user_id,
        name=req.name,
        email=req.email,
        linkedin_url=req.linkedin_url,
        resume_text=req.resume_text,
        target_role=req.target_role,
        target_companies=req.target_companies,
        years_of_experience=req.years_of_experience,
        created_at=now,
        updated_at=now,
    )
    save_profile(profile)
    return profile


def save_profile(profile: UserProfile) -> None:
    profile.updated_at = datetime.now(timezone.utc).isoformat()
    with open(_user_path(profile.user_id), "w") as f:
        json.dump(profile.model_dump(), f, indent=2)


def get_profile(user_id: str) -> Optional[UserProfile]:
    path = _user_path(user_id)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return UserProfile(**json.load(f))


def list_profiles() -> list[UserProfile]:
    profiles = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(DATA_DIR, fname)) as f:
                profiles.append(UserProfile(**json.load(f)))
    return profiles
