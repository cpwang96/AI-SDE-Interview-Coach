import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from models.schemas import StartSessionRequest, ChatRequest, ChatResponse
from services.ai_coach import chat_with_coach, CODING_SYSTEM_PROMPT
from services.question_bank import get_question, list_questions, get_all_tags
from services.question_generator import generate_question, get_generated_questions, generate_study_session
from services.code_runner import execute_code
from services.submission_store import save_submission, get_solved_questions, get_latest_submission, load_submissions

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


def _get_expected(tc: dict):
    """Normalize test case — support both 'expected' and 'expected_output' keys."""
    return tc.get("expected_output", tc.get("expected"))


def _build_test_runner_python(func_name: str, test_cases: list[dict]) -> str:
    """Auto-generate a Python test runner from test_cases."""
    lines = ["", "", "# --- Auto-generated test runner ---"]
    lines.append("def _run_tests():")
    lines.append("    _passed = 0")
    lines.append(f"    _total = {len(test_cases)}")

    for i, tc in enumerate(test_cases):
        args = ", ".join(repr(v) for v in tc["input"].values())
        expected = repr(_get_expected(tc))
        lines.append(f"    _result = {func_name}({args})")
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
        expected = _js_repr(_get_expected(tc))
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


def _java_type(val) -> str:
    """Infer Java type from a Python value."""
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "int"
    if isinstance(val, float):
        return "double"
    if isinstance(val, str):
        return "String"
    if isinstance(val, list):
        if not val:
            return "int[]"
        if isinstance(val[0], list):
            inner = val[0]
            return "String[][]" if (inner and isinstance(inner[0], str)) else "int[][]"
        if isinstance(val[0], str):
            return "String[]"
        if isinstance(val[0], bool):
            return "boolean[]"
        return "int[]"
    return "Object"


def _java_val(val) -> str:
    """Convert a Python value to a Java literal expression."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        return str(val)
    if isinstance(val, float):
        return str(val)
    if isinstance(val, str):
        escaped = val.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(val, list):
        if not val:
            return "new int[]{}"
        if isinstance(val[0], list):
            inner_base = "String" if (val[0] and isinstance(val[0][0], str)) else "int"
            rows = ", ".join(
                f"new {inner_base}[]{{{', '.join(_java_val(x) for x in row)}}}"
                for row in val
            )
            return f"new {inner_base}[][]{{{rows}}}"
        if isinstance(val[0], str):
            inner = ", ".join(f'"{x}"' for x in val)
            return f"new String[]{{{inner}}}"
        if isinstance(val[0], bool):
            inner = ", ".join("true" if x else "false" for x in val)
            return f"new boolean[]{{{inner}}}"
        inner = ", ".join(str(x) for x in val)
        return f"new int[]{{{inner}}}"
    return str(val)


def _java_equals(a: str, b: str, val) -> str:
    """Generate Java equality expression for two variables."""
    if isinstance(val, list):
        if val and isinstance(val[0], list):
            return f"java.util.Arrays.deepEquals({a}, {b})"
        return f"java.util.Arrays.equals({a}, {b})"
    if isinstance(val, str):
        return f"{a}.equals({b})"
    return f"({a} == {b})"


def _java_to_str(var: str, val) -> str:
    """Generate Java expression to convert a value to a display string."""
    if isinstance(val, list):
        if val and isinstance(val[0], list):
            return f"java.util.Arrays.deepToString({var})"
        return f"java.util.Arrays.toString({var})"
    return f"String.valueOf({var})"


def _build_test_runner_java(func_name: str, test_cases: list[dict]) -> str:
    """Auto-generate a Java Main class test runner from test_cases."""
    lines = ["", "", "public class Main {",
             "    public static void main(String[] args) {",
             "        Solution sol = new Solution();",
             "        int passed = 0;",
             f"        int total = {len(test_cases)};"]

    for i, tc in enumerate(test_cases):
        n = i + 1
        expected = _get_expected(tc)
        exp_type = _java_type(expected)
        exp_lit = _java_val(expected)
        exp_var = f"exp{n}"
        res_var = f"res{n}"

        # Declare input args
        arg_vars = []
        for j, (key, val) in enumerate(tc["input"].items()):
            vname = f"a{n}_{j}"
            lines.append(f"        {_java_type(val)} {vname} = {_java_val(val)};")
            arg_vars.append(vname)

        # Declare expected and call method
        lines.append(f"        {exp_type} {exp_var} = {exp_lit};")
        lines.append(f"        {exp_type} {res_var} = sol.{func_name}({', '.join(arg_vars)});")

        # Compare and print
        eq_expr = _java_equals(res_var, exp_var, expected)
        res_str = _java_to_str(res_var, expected)
        exp_str = _java_to_str(exp_var, expected)
        input_display = ", ".join(str(v) for v in tc["input"].values())
        lines.append(f"        boolean ok{n} = {eq_expr};")
        lines.append(f"        if (ok{n}) passed++;")
        lines.append(
            f'        System.out.println("Test {n}: " + (ok{n} ? "PASS" : "FAIL")'
            f' + " | Input: {input_display} | Expected: " + {exp_str} + " | Got: " + {res_str});'
        )

    lines.append(f'        System.out.println("\\n" + passed + "/{len(test_cases)} tests passed");')
    lines.append("    }")
    lines.append("}")
    return "\n".join(lines)


def _extract_func_name(code: str, language: str) -> str:
    """Extract the main function/method name from starter code."""
    import re
    if language == "python":
        match = re.search(r'^def\s+(\w+)\s*\(', code, re.MULTILINE)
        if match:
            return match.group(1)
    elif language == "javascript":
        match = re.search(r'function\s+(\w+)\s*\(', code)
        if match:
            return match.group(1)
    elif language == "java":
        # Match: public <ReturnType> methodName( — skip constructors and main
        for m in re.finditer(r'public\s+[\w\[\]<>, ]+?\s+(\w+)\s*\(', code):
            name = m.group(1)
            if name not in ("Solution", "Main", "main", "Codec", "WordDictionary",
                            "MedianFinder", "Trie", "LRUCache"):
                return name
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
        elif req.language == "java":
            test_code += _build_test_runner_java(func_name, question["test_cases"])

    result = execute_code(test_code, req.language)

    lines = result.stdout.strip().split("\n") if result.stdout else []
    passed = sum(1 for l in lines if "PASS" in l)
    failed = sum(1 for l in lines if "FAIL" in l)
    total = passed + failed

    # If no tests ran but there was an error, surface it clearly
    stderr = result.stderr or ""
    if total == 0 and result.exit_code != 0 and stderr:
        stderr = f"Execution failed — no tests ran.\n\n{stderr}"

    all_passed = total > 0 and failed == 0

    # Persist submission
    user_id = getattr(req, "user_id", "default") if hasattr(req, "user_id") else "default"
    save_submission(
        user_id=user_id,
        question_id=req.question_id,
        code=req.code,
        language=req.language,
        passed=passed,
        total=total,
        all_passed=all_passed,
    )

    return {
        "stdout": result.stdout,
        "stderr": stderr,
        "exit_code": result.exit_code,
        "time_ms": result.time_ms,
        "passed": passed,
        "failed": failed,
        "total": total,
        "all_passed": all_passed,
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


@router.get("/solved")
def get_solved(user_id: str = "default"):
    """Return list of question IDs the user has solved."""
    return get_solved_questions(user_id)


@router.get("/submissions/{question_id}")
def get_submission(question_id: str, user_id: str = "default"):
    """Return the latest submission for a question."""
    sub = get_latest_submission(user_id, question_id)
    if sub:
        return sub
    return {"error": "No submission found"}


@router.get("/submissions")
def get_all_submissions(user_id: str = "default"):
    """Return all submissions for a user."""
    return load_submissions(user_id)
