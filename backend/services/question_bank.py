import json
import os
import random
from typing import Optional
from models.schemas import CodingQuestion

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_questions() -> list[CodingQuestion]:
    path = os.path.join(DATA_DIR, "coding_questions.json")
    with open(path) as f:
        data = json.load(f)
    return [CodingQuestion(**q) for q in data]


def get_question(
    question_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
) -> CodingQuestion:
    questions = load_questions()

    if question_id:
        for q in questions:
            if q.id == question_id:
                return q
        raise ValueError(f"Question {question_id} not found")

    filtered = questions
    if difficulty:
        filtered = [q for q in filtered if q.difficulty == difficulty]
    if topic:
        filtered = [q for q in filtered if topic.lower() in [t.lower() for t in q.tags]]

    if not filtered:
        filtered = questions

    return random.choice(filtered)


def list_questions(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
) -> list[CodingQuestion]:
    questions = load_questions()
    if difficulty:
        questions = [q for q in questions if q.difficulty == difficulty]
    if topic:
        questions = [q for q in questions if topic.lower() in [t.lower() for t in q.tags]]
    return questions
