from github import Github
from base64 import b64decode
import re, os

def get_latest_code(filepath, repo_name, branch):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GITHUB_TOKEN environment variable")

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    try:
        contents = repo.get_contents(filepath, ref=branch)
    except Exception:
        return "<No content>"
    file_content = b64decode(contents.content).decode("utf-8")
    return file_content

def extract_python_code(text: str):
    """Extract Python code block from an LLM response."""
    code_match = re.search(r"```(?:python)?\s*\n([\s\S]*?)\n?```", text, re.IGNORECASE)
    if code_match:
        return code_match.group(1).strip()
    if re.search(r'\b(def|class|import|from|if __name__|async|await)\b', text):
        return text.strip()
    return text.strip()
