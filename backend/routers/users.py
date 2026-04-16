import uuid
from fastapi import APIRouter, HTTPException

from models.schemas import CreateProfileRequest, UserProfile
from services.user_service import create_profile, get_profile, list_profiles

router = APIRouter()


@router.post("/profile", response_model=UserProfile)
def create_user_profile(req: CreateProfileRequest):
    user_id = str(uuid.uuid4())[:8]
    return create_profile(user_id, req)


@router.get("/profile/{user_id}", response_model=UserProfile)
def get_user_profile(user_id: str):
    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile


@router.get("/profiles")
def get_all_profiles():
    return [{"user_id": p.user_id, "name": p.name} for p in list_profiles()]
