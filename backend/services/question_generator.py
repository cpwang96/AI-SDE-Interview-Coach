import json
import os
from datetime import datetime, timezone
from typing import Optional

from services.ai_coach import client

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "generated")
os.makedirs(DATA_DIR, exist_ok=True)

GENERATE_PROMPT = """You are an expert coding interview question designer. Generate a coding interview question based on the requirements below.

Requirements:
- Topic: {topic}
- Difficulty: {difficulty}
- The question should be original but similar in style to LeetCode/HackerRank problems
{context}

Respond with ONLY valid JSON in this exact format (no markdown, no code blocks):
{{
  "id": "short-kebab-case-id",
  "title": "Question Title",
  "difficulty": "{difficulty}",
  "description": "Full problem description with clear explanation. Use markdown for formatting.",
  "examples": [
    {{"input": "descriptive input", "output": "expected output", "explanation": "why"}},
    {{"input": "another input", "output": "expected output", "explanation": ""}}
  ],
  "constraints": ["constraint 1", "constraint 2"],
  "starter_code": {{
    "python": "def solution_func(params):\\n    # Your code here\\n    pass\\n\\n# --- Test your solution ---\\nprint(solution_func(test_input))",
    "javascript": "function solutionFunc(params) {{\\n    // Your code here\\n}}\\n\\n// --- Test your solution ---\\nconsole.log(solutionFunc(testInput));",
    "java": "public class Solution {{\\n    public static returnType solutionFunc(params) {{\\n        // Your code here\\n    }}\\n\\n    public static void main(String[] args) {{\\n        System.out.println(solutionFunc(testInput));\\n    }}\\n}}"
  }},
  "test_runner": {{
    "python": "import json\\ndef test():\\n    cases = [\\n        (input1, expected1),\\n        (input2, expected2),\\n        (input3, expected3),\\n        (input4, expected4),\\n        (input5, expected5)\\n    ]\\n    passed = 0\\n    for i, (inp, expected) in enumerate(cases):\\n        result = solution_func(inp)  # call the user's function\\n        status = 'PASS' if result == expected else 'FAIL'\\n        if status == 'PASS':\\n            passed += 1\\n        print(f'Test {{i+1}}: {{status}} | Input: {{inp}} | Expected: {{expected}} | Got: {{result}}')\\n    print(f'\\\\n{{passed}}/{{len(cases)}} tests passed')\\ntest()",
    "javascript": "function test() {{\\n    const cases = [\\n        [input1, expected1],\\n        [input2, expected2],\\n        [input3, expected3],\\n        [input4, expected4],\\n        [input5, expected5]\\n    ];\\n    let passed = 0;\\n    cases.forEach(([inp, expected], i) => {{\\n        const result = solutionFunc(inp);\\n        const status = JSON.stringify(result) === JSON.stringify(expected) ? 'PASS' : 'FAIL';\\n        if (status === 'PASS') passed++;\\n        console.log(`Test ${{i+1}}: ${{status}} | Input: ${{JSON.stringify(inp)}} | Expected: ${{JSON.stringify(expected)}} | Got: ${{JSON.stringify(result)}}`);\\n    }});\\n    console.log(`\\\\n${{passed}}/${{cases.length}} tests passed`);\\n}}\\ntest();",
    "java": "// test runner integrated into main method"
  }},
  "tags": ["tag1", "tag2"],
  "hints": [
    "A small hint that nudges toward the right approach",
    "A bigger hint that reveals more of the strategy",
    "The key insight needed to solve optimally"
  ],
  "optimal_complexity": {{
    "time": "O(...)",
    "space": "O(...)"
  }}
}}

IMPORTANT:
- The test_runner code must be a COMPLETE runnable test that calls the user's function
- Include at least 5 test cases covering normal cases, edge cases, and boundary conditions
- The starter_code should include test prints so users can run and see output immediately
- Make the Java class name "Solution" always
- Ensure the question is solvable and well-defined
"""


def generate_question(
    topic: str,
    difficulty: str,
    user_context: str = "",
) -> dict:
    """Use Claude to generate a new coding question with test cases."""
    context = ""
    if user_context:
        context = f"- User context: {user_context}"

    prompt = GENERATE_PROMPT.format(
        topic=topic,
        difficulty=difficulty,
        context=context,
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    # Strip markdown code block if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]

    question = json.loads(text)

    # Save to generated questions
    _save_generated(question)

    return question


def _save_generated(question: dict) -> None:
    """Persist generated question to disk."""
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fname = f"{date}_{question['id']}.json"
    with open(os.path.join(DATA_DIR, fname), "w") as f:
        json.dump(question, f, indent=2)


def get_generated_questions() -> list[dict]:
    """List all previously generated questions."""
    questions = []
    for fname in sorted(os.listdir(DATA_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(DATA_DIR, fname)) as f:
                questions.append(json.load(f))
    return questions


def generate_study_session(
    weak_topics: list[str],
    level: str = "intermediate",
    num_questions: int = 3,
) -> list[dict]:
    """Generate a set of questions for a study session based on weak areas."""
    questions = []
    difficulties = {
        "beginner": ["easy", "easy", "medium"],
        "intermediate": ["easy", "medium", "medium"],
        "advanced": ["medium", "medium", "hard"],
    }
    diffs = difficulties.get(level, difficulties["intermediate"])

    for i, topic in enumerate(weak_topics[:num_questions]):
        diff = diffs[i] if i < len(diffs) else "medium"
        q = generate_question(topic, diff)
        questions.append(q)

    return questions
