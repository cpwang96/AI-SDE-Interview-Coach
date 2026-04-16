from pydantic import BaseModel
from typing import Optional


class CodingQuestion(BaseModel):
    id: str
    title: str
    difficulty: str  # easy, medium, hard
    description: str
    examples: list[dict]
    constraints: list[str]
    starter_code: dict[str, str]  # language -> starter code
    test_cases: list[dict] = []
    tags: list[str]  # algorithm tags: array, hash-table, two-pointers, etc.
    companies: list[str] = []  # company tags: google, meta, amazon, etc.
    frequency: str = "medium"  # high, medium, low — how often asked in interviews
    category: str = ""  # blind75, neetcode150, etc.


class StartSessionRequest(BaseModel):
    question_id: Optional[str] = None
    difficulty: Optional[str] = None
    topic: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: str
    message: str
    code: Optional[str] = None
    language: Optional[str] = "python"


class ChatResponse(BaseModel):
    response: str
    hints: Optional[list[str]] = None


class ExecuteRequest(BaseModel):
    code: str
    language: str
    test_cases: Optional[list[dict]] = None


class ExecuteResult(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    time_ms: Optional[float] = None


class SystemDesignRequest(BaseModel):
    topic: Optional[str] = None
    difficulty: Optional[str] = None


class SystemDesignMessage(BaseModel):
    session_id: str
    message: str


# --- User Profile ---

class UserProfile(BaseModel):
    user_id: str
    name: str
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_text: Optional[str] = None
    target_role: Optional[str] = None  # e.g. "Senior SDE", "Staff Engineer"
    target_companies: list[str] = []
    years_of_experience: Optional[int] = None
    strongest_topics: list[str] = []
    weakest_topics: list[str] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class CreateProfileRequest(BaseModel):
    name: str
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_text: Optional[str] = None
    target_role: Optional[str] = None
    target_companies: list[str] = []
    years_of_experience: Optional[int] = None


# --- Assessment ---

class AssessmentProblem(BaseModel):
    question_id: str
    topic: str
    difficulty: str
    completed: bool = False
    user_code: Optional[str] = None
    coach_evaluation: Optional[str] = None
    score: Optional[int] = None  # 0-100


class AssessmentResult(BaseModel):
    user_id: str
    problems: list[AssessmentProblem] = []
    overall_level: Optional[str] = None  # beginner, intermediate, advanced
    topic_scores: dict[str, int] = {}  # topic -> score
    study_plan: Optional[str] = None
    assessed_at: Optional[str] = None


class AssessmentSubmission(BaseModel):
    user_id: str
    question_id: str
    code: str
    language: str = "python"


# --- Session Persistence ---

class SavedSession(BaseModel):
    session_id: str
    user_id: str
    question_id: Optional[str] = None
    session_type: str  # "coding" or "system_design"
    messages: list[dict] = []
    final_code: Optional[str] = None
    language: Optional[str] = None
    outcome: Optional[str] = None  # "solved", "partially_solved", "gave_up"
    started_at: str
    ended_at: Optional[str] = None
