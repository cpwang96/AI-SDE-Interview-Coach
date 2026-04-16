import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from models.schemas import StartSessionRequest, ChatRequest, ChatResponse
from services.ai_coach import chat_with_coach, CODING_SYSTEM_PROMPT
from services.question_bank import get_question, list_questions, get_all_tags
from services.question_generator import generate_question, get_generated_questions, generate_study_session
from services.code_runner import execute_code

router = APIRouter()


class SubmitRequest(BaseModel):
    session_id: str
    code: str
    language: str
    question_id: str


class GenerateRequest(BaseModel):
    topic: str = "array"
    difficulty: str = "medium"
    context: str = ""


class GenerateSessionRequest(BaseModel):
    weak_topics: list[str]
    level: str = "intermediate"
    num_questions: int = 3


@router.get("/questions")
def get_questions(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    company: Optional[str] = None,
    frequency: Optional[str] = None,
    category: Optional[str] = None,
):
    static = list_questions(difficulty=difficulty, topic=topic, company=company, frequency=frequency, category=category)
    static_list = [{
        "id": q.id, "title": q.title, "difficulty": q.difficulty,
        "tags": q.tags, "companies": q.companies, "frequency": q.frequency,
        "category": q.category, "source": "bank",
    } for q in static]

    generated = get_generated_questions()
    if difficulty:
        generated = [q for q in generated if q.get("difficulty") == difficulty]
    if topic:
        generated = [q for q in generated if topic.lower() in [t.lower() for t in q.get("tags", [])]]
    gen_list = [{
        "id": q["id"], "title": q["title"], "difficulty": q["difficulty"],
        "tags": q.get("tags", []), "companies": [], "frequency": "medium",
        "category": "generated", "source": "generated",
    } for q in generated]

    return static_list + gen_list


@router.get("/filters")
def get_filters():
    """Return all available filter options for the UI."""
    return get_all_tags()


@router.post("/generate")
def generate_new_question(req: GenerateRequest):
    question = generate_question(req.topic, req.difficulty, req.context)
    return question


@router.post("/generate-session")
def generate_session(req: GenerateSessionRequest):
    questions = generate_study_session(req.weak_topics, req.level, req.num_questions)
    return {"questions": questions}


@router.post("/start")
def start_session(req: StartSessionRequest):
    question = None

    if req.question_id:
        generated = get_generated_questions()
        for gq in generated:
            if gq["id"] == req.question_id:
                question = gq
                break
        if not question:
            q = get_question(question_id=req.question_id)
            question = q.model_dump()
    else:
        q = get_question(difficulty=req.difficulty, topic=req.topic)
        question = q.model_dump()

    session_id = str(uuid.uuid4())

    intro = f"The candidate is working on: **{question['title']}** ({question['difficulty']})\n\n"
    intro += f"{question['description']}\n\n"
    intro += "Examples:\n"
    for ex in question.get("examples", []):
        intro += f"- Input: {ex['input']}\n  Output: {ex['output']}\n"
    constraints = question.get("constraints", [])
    if constraints:
        intro += f"\nConstraints: {', '.join(constraints)}\n"
    intro += "\nPresent the problem to the candidate and ask them how they'd approach it."

    # Try Claude coach, but don't fail if API is unavailable
    try:
        response = chat_with_coach(session_id, intro, CODING_SYSTEM_PROMPT)
    except Exception:
        response = f"**{question['title']}** ({question['difficulty']})\n\nTake your time to understand the problem. When you're ready, write your solution and hit **Submit** to run it against the test cases.\n\n*AI coach is unavailable — add Anthropic API credits to enable coaching.*"

    return {
        "session_id": session_id,
        "question": question,
        "coach_message": response,
    }


def _build_test_runner_python(func_name: str, test_cases: list[dict]) -> str:
    """Auto-generate a Python test runner from test_cases."""
    lines = ["", "", "# --- Auto-generated test runner ---"]
    lines.append("import json")
    lines.append("def _run_tests():")
    lines.append("    _passed = 0")
    lines.append(f"    _total = {len(test_cases)}")

    for i, tc in enumerate(test_cases):
        args = ", ".join(repr(v) for v in tc["input"].values())
        expected = repr(tc["expected"])
        lines.append(f"    _result = {func_name}({args})")
        # Sort lists for comparison if both are lists
        lines.append(f"    _exp = {expected}")
        lines.append(f"    _eq = (sorted(_result) == sorted(_exp)) if isinstance(_result, list) and isinstance(_exp, list) else (_result == _exp)")
        lines.append(f'    _status = "PASS" if _eq else "FAIL"')
        lines.append(f"    if _eq: _passed += 1")
        lines.append(f'    print(f"Test {i+1}: {{_status}} | Input: {args} | Expected: {{_exp}} | Got: {{_result}}")')

    lines.append(f'    print(f"\\n{{_passed}}/{{_total}} tests passed")')
    lines.append("_run_tests()")
    return "\n".join(lines)


def _build_test_runner_js(func_name: str, test_cases: list[dict]) -> str:
    """Auto-generate a JavaScript test runner from test_cases."""
    lines = ["", "", "// --- Auto-generated test runner ---"]
    lines.append("(function() {")
    lines.append("  let passed = 0;")

    for i, tc in enumerate(test_cases):
        args = ", ".join(_js_repr(v) for v in tc["input"].values())
        expected = _js_repr(tc["expected"])
        lines.append(f"  const r{i} = {func_name}({args});")
        lines.append(f"  const e{i} = {expected};")
        lines.append(f"  const ok{i} = JSON.stringify(Array.isArray(r{i}) ? [...r{i}].sort() : r{i}) === JSON.stringify(Array.isArray(e{i}) ? [...e{i}].sort() : e{i});")
        lines.append(f'  if (ok{i}) passed++;')
        lines.append(f'  console.log(`Test {i+1}: ${{ok{i} ? "PASS" : "FAIL"}} | Input: {args} | Expected: ${{JSON.stringify(e{i})}} | Got: ${{JSON.stringify(r{i})}}`);')

    lines.append(f'  console.log(`\\n${{passed}}/{len(test_cases)} tests passed`);')
    lines.append("})();")
    return "\n".join(lines)


def _js_repr(val) -> str:
    """Convert Python value to JavaScript literal."""
    import json
    return json.dumps(val)


def _extract_func_name(code: str, language: str) -> str:
    """Extract the main function name from starter code."""
    import re
    if language == "python":
        match = re.search(r'^def\s+(\w+)\s*\(', code, re.MULTILINE)
        if match:
            return match.group(1)
    elif language in ("javascript", "java"):
        match = re.search(r'function\s+(\w+)\s*\(', code)
        if match:
            return match.group(1)
    return "solution"


@router.post("/submit")
def submit_solution(req: SubmitRequest):
    """Run code against test cases and return pass/fail results."""
    question = None
    generated = get_generated_questions()
    for gq in generated:
        if gq["id"] == req.question_id:
            question = gq
            break

    if not question:
        try:
            q = get_question(question_id=req.question_id)
            question = q.model_dump()
        except ValueError:
            pass

    if not question:
        result = execute_code(req.code, req.language)
        return {
            "stdout": result.stdout, "stderr": result.stderr,
            "exit_code": result.exit_code, "time_ms": result.time_ms,
            "passed": 0, "failed": 0, "total": 0, "all_passed": False,
        }

    # Build test code: user's solution + test runner
    test_code = req.code

    # Strip any existing test prints from user code (everything after "# --- Test")
    for marker in ["# --- Test", "// --- Test"]:
        if marker in test_code:
            test_code = test_code[:test_code.index(marker)].rstrip()

    # Use explicit test_runner if available (generated questions have these)
    if question.get("test_runner", {}).get(req.language):
        test_code += "\n\n" + question["test_runner"][req.language]
    elif question.get("test_cases"):
        # Auto-build test runner from test_cases (static bank questions)
        func_name = _extract_func_name(question.get("starter_code", {}).get(req.language, ""), req.language)
        if req.language == "python":
            test_code += _build_test_runner_python(func_name, question["test_cases"])
        elif req.language == "javascript":
            test_code += _build_test_runner_js(func_name, question["test_cases"])

    result = execute_code(test_code, req.language)

    lines = result.stdout.strip().split("\n") if result.stdout else []
    passed = sum(1 for l in lines if "PASS" in l)
    failed = sum(1 for l in lines if "FAIL" in l)
    total = passed + failed

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.exit_code,
        "time_ms": result.time_ms,
        "passed": passed,
        "failed": failed,
        "total": total,
        "all_passed": total > 0 and failed == 0,
    }


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        response = chat_with_coach(
            session_id=req.session_id,
            user_message=req.message,
            system_prompt=CODING_SYSTEM_PROMPT,
            code=req.code,
            language=req.language,
        )
    except Exception:
        response = "*AI coach is unavailable. Please check your Anthropic API credits at console.anthropic.com.*"
    return ChatResponse(response=response)
