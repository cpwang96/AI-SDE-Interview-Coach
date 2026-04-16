import subprocess
import tempfile
import os
import time
from models.schemas import ExecuteResult

LANGUAGE_CONFIG = {
    "python": {
        "extension": ".py",
        "command": ["python3"],
    },
    "javascript": {
        "extension": ".js",
        "command": ["node"],
    },
    "java": {
        "extension": ".java",
        "command": None,  # special handling — compile then run
    },
}

TIMEOUT_SECONDS = 10


def _run_java(code: str, stdin: str = "") -> ExecuteResult:
    """Compile and run Java code. Extracts class name from code."""
    import re
    match = re.search(r'public\s+class\s+(\w+)', code)
    class_name = match.group(1) if match else "Solution"

    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, f"{class_name}.java")
        with open(src_path, "w") as f:
            f.write(code)

        # Compile
        try:
            compile_result = subprocess.run(
                ["javac", src_path],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            if compile_result.returncode != 0:
                return ExecuteResult(
                    stdout="",
                    stderr=f"Compilation Error:\n{compile_result.stderr}",
                    exit_code=compile_result.returncode,
                )
        except FileNotFoundError:
            return ExecuteResult(
                stdout="",
                stderr="Java compiler (javac) not found. Install JDK: brew install openjdk",
                exit_code=1,
            )
        except subprocess.TimeoutExpired:
            return ExecuteResult(stdout="", stderr="Compilation timed out", exit_code=124)

        # Run
        try:
            start = time.time()
            run_result = subprocess.run(
                ["java", "-cp", tmpdir, class_name],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            elapsed = (time.time() - start) * 1000
            return ExecuteResult(
                stdout=run_result.stdout,
                stderr=run_result.stderr,
                exit_code=run_result.returncode,
                time_ms=round(elapsed, 2),
            )
        except subprocess.TimeoutExpired:
            return ExecuteResult(
                stdout="",
                stderr=f"Time Limit Exceeded ({TIMEOUT_SECONDS}s)",
                exit_code=124,
            )


def execute_code(code: str, language: str, stdin: str = "") -> ExecuteResult:
    config = LANGUAGE_CONFIG.get(language)
    if not config:
        return ExecuteResult(
            stdout="",
            stderr=f"Unsupported language: {language}. Supported: {', '.join(LANGUAGE_CONFIG.keys())}",
            exit_code=1,
        )

    if language == "java":
        return _run_java(code, stdin)

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
