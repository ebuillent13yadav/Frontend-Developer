import subprocess
from src.state import ProjectState
import shutil

def build_verifier_node(state: ProjectState):
    npm_path = shutil.which("npm") or shutil.which("npm.cmd")
    result = subprocess.run(
        [npm_path, "run", "build"],
        cwd="./my-generated-app",
        capture_output=True,
        text=True,
    )

    return {
        "build_passed": result.returncode == 0,
        "build_error": result.stderr,
        "build_attempts": state.get("build_attempts",0) + 1,
    }

    # Nagar Nigam Pratibha Vidyalay Mandoli Vistar Saboli Delhi-110093