import uuid
from fastapi import APIRouter
from typing import Optional

from models.schemas import StartSessionRequest, ChatRequest, ChatResponse
from services.ai_coach import chat_with_coach, CODING_SYSTEM_PROMPT
from services.question_bank import get_question, list_questions

router = APIRouter()


@router.get("/questions")
def get_questions(difficulty: Optional[str] = None, topic: Optional[str] = None):
    questions = list_questions(difficulty=difficulty, topic=topic)
    return [{"id": q.id, "title": q.title, "difficulty": q.difficulty, "tags": q.tags} for q in questions]


@router.post("/start")
def start_session(req: StartSessionRequest):
    question = get_question(
        question_id=req.question_id,
        difficulty=req.difficulty,
        topic=req.topic,
    )
    session_id = str(uuid.uuid4())

    # Prime the coach with the question context
    intro = f"The candidate is working on: **{question.title}** ({question.difficulty})\n\n"
    intro += f"{question.description}\n\n"
    intro += "Examples:\n"
    for ex in question.examples:
        intro += f"- Input: {ex['input']}\n  Output: {ex['output']}\n"
    intro += f"\nConstraints: {', '.join(question.constraints)}\n"
    intro += "\nPresent the problem to the candidate and ask them how they'd approach it."

    response = chat_with_coach(session_id, intro, CODING_SYSTEM_PROMPT)

    return {
        "session_id": session_id,
        "question": question.model_dump(),
        "coach_message": response,
    }


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    response = chat_with_coach(
        session_id=req.session_id,
        user_message=req.message,
        system_prompt=CODING_SYSTEM_PROMPT,
        code=req.code,
        language=req.language,
    )
    return ChatResponse(response=response)
