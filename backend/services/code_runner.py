import subprocess
import tempfile
import os
import time
from models.schemas import ExecuteResult

# Language configs for local execution (no Judge0 needed for MVP)
LANGUAGE_CONFIG = {
    "python": {
        "extension": ".py",
        "command": ["python3"],
    },
    "javascript": {
        "extension": ".js",
        "command": ["node"],
    },
}

TIMEOUT_SECONDS = 10


def execute_code(code: str, language: str, stdin: str = "") -> ExecuteResult:
    config = LANGUAGE_CONFIG.get(language)
    if not config:
        return ExecuteResult(
            stdout="",
            stderr=f"Unsupported language: {language}. Supported: {', '.join(LANGUAGE_CONFIG.keys())}",
            exit_code=1,
        )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=config["extension"],
        delete=False,
    ) as f:
        f.write(code)
        f.flush()
        temp_path = f.name

    try:
        start = time.time()
        result = subprocess.run(
            config["command"] + [temp_path],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        elapsed = (time.time() - start) * 1000

        return ExecuteResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            time_ms=round(elapsed, 2),
        )
    except subprocess.TimeoutExpired:
        return ExecuteResult(
            stdout="",
            stderr=f"Time Limit Exceeded ({TIMEOUT_SECONDS}s)",
            exit_code=124,
        )
    finally:
        os.unlink(temp_path)
