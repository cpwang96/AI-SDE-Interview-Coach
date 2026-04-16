import json
import os
from datetime import datetime, timezone
from typing import Optional

from models.schemas import AssessmentResult, AssessmentProblem, AssessmentSubmission
from services.ai_coach import chat_with_coach

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "assessments")

# Topics and difficulties to cover in assessment
ASSESSMENT_PLAN = [
    {"topic": "array", "difficulty": "easy", "question_id": "two-sum"},
    {"topic": "string", "difficulty": "easy", "question_id": "valid-parentheses"},
    {"topic": "sorting", "difficulty": "medium", "question_id": "merge-intervals"},
    {"topic": "design", "difficulty": "medium", "question_id": "lru-cache"},
    {"topic": "binary-search", "difficulty": "hard", "question_id": "median-sorted-arrays"},
    {"topic": "bfs", "difficulty": "hard", "question_id": "word-ladder"},
]

EVALUATION_PROMPT = """You are evaluating a coding interview candidate's solution.
Analyze the code and provide:
1. A score from 0-100 based on correctness, efficiency, and code quality
2. A brief evaluation (2-3 sentences)

Scoring guide:
- 90-100: Optimal solution, clean code, handles edge cases
- 70-89: Correct solution, reasonable complexity, minor issues
- 50-69: Partially correct, brute force or missing edge cases
- 30-49: On the right track but significant issues
- 0-29: Incorrect approach or barely started

Respond in this exact JSON format:
{"score": <number>, "evaluation": "<text>"}
"""

STUDY_PLAN_PROMPT = """You are an expert coding interview coach. Based on the candidate's assessment results below, create a personalized 2-week study plan.

Assessment Results:
{results}

User Background:
{background}

Create a structured study plan that:
1. Prioritizes their weakest topics
2. Gradually increases difficulty
3. Includes specific problem types to practice
4. Suggests daily time commitment
5. Includes review days

Format the plan clearly with days and specific topics/problem types.
"""


def _assessment_path(user_id: str) -> str:
    return os.path.join(DATA_DIR, f"{user_id}.json")


def get_assessment(user_id: str) -> Optional[AssessmentResult]:
    path = _assessment_path(user_id)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return AssessmentResult(**json.load(f))


def save_assessment(result: AssessmentResult) -> None:
    with open(_assessment_path(result.user_id), "w") as f:
        json.dump(result.model_dump(), f, indent=2)


def start_assessment(user_id: str) -> AssessmentResult:
    problems = [
        AssessmentProblem(
            question_id=p["question_id"],
            topic=p["topic"],
            difficulty=p["difficulty"],
        )
        for p in ASSESSMENT_PLAN
    ]
    result = AssessmentResult(
        user_id=user_id,
        problems=problems,
        assessed_at=datetime.now(timezone.utc).isoformat(),
    )
    save_assessment(result)
    return result


def evaluate_submission(submission: AssessmentSubmission, question_title: str) -> dict:
    """Use Claude to evaluate a code submission and return score + evaluation."""
    prompt = f"Question: {question_title}\nLanguage: {submission.language}\n\nCode:\n```{submission.language}\n{submission.code}\n```"

    session_id = f"eval_{submission.user_id}_{submission.question_id}"
    response = chat_with_coach(session_id, prompt, EVALUATION_PROMPT)

    try:
        # Parse the JSON response
        result = json.loads(response)
        return {"score": result["score"], "evaluation": result["evaluation"]}
    except (json.JSONDecodeError, KeyError):
        return {"score": 0, "evaluation": response}


def generate_study_plan(user_id: str, background: str = "") -> str:
    """Generate a personalized study plan based on assessment results."""
    assessment = get_assessment(user_id)
    if not assessment:
        return "No assessment found. Please complete the assessment first."

    results_text = ""
    for p in assessment.problems:
        results_text += f"- {p.topic} ({p.difficulty}): "
        if p.completed:
            results_text += f"Score {p.score}/100 — {p.coach_evaluation}\n"
        else:
            results_text += "Not attempted\n"

    prompt = STUDY_PLAN_PROMPT.format(results=results_text, background=background)
    session_id = f"plan_{user_id}"
    return chat_with_coach(session_id, "Generate my study plan.", prompt)
