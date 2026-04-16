import uuid
from fastapi import APIRouter

from models.schemas import SystemDesignRequest, SystemDesignMessage, ChatResponse
from services.ai_coach import chat_with_coach, SYSTEM_DESIGN_PROMPT

router = APIRouter()

SYSTEM_DESIGN_TOPICS = [
    "Design a URL Shortener (like bit.ly)",
    "Design a Chat Application (like WhatsApp/Slack)",
    "Design a News Feed (like Twitter/Facebook)",
    "Design a Video Streaming Service (like YouTube/Netflix)",
    "Design a Ride-Sharing Service (like Uber/Lyft)",
    "Design a Search Engine",
    "Design a Rate Limiter",
    "Design a Key-Value Store",
    "Design a Notification System",
    "Design a File Storage Service (like Google Drive/Dropbox)",
]


@router.get("/topics")
def get_topics():
    return [{"id": i, "title": t} for i, t in enumerate(SYSTEM_DESIGN_TOPICS)]


@router.post("/start")
def start_session(req: SystemDesignRequest):
    session_id = str(uuid.uuid4())

    if req.topic:
        prompt = f"Start a system design interview on the topic: {req.topic}. Present the problem and ask the candidate to begin with requirements gathering."
    else:
        import random
        topic = random.choice(SYSTEM_DESIGN_TOPICS)
        prompt = f"Start a system design interview on the topic: {topic}. Present the problem and ask the candidate to begin with requirements gathering."

    response = chat_with_coach(session_id, prompt, SYSTEM_DESIGN_PROMPT)

    return {
        "session_id": session_id,
        "coach_message": response,
    }


@router.post("/chat", response_model=ChatResponse)
def chat(req: SystemDesignMessage):
    response = chat_with_coach(
        session_id=req.session_id,
        user_message=req.message,
        system_prompt=SYSTEM_DESIGN_PROMPT,
    )
    return ChatResponse(response=response)
