import time
import base64
import jwt
import requests
from pathlib import Path
from typing import Dict, Optional


GITHUB_API = "https://api.github.com"


# -----------------------------
# Auth
# -----------------------------

def generate_jwt(app_id: str, private_key: str) -> str:
    payload = {
        "iat": int(time.time()) - 60,
        "exp": int(time.time()) + 600,
        "iss": app_id,
    }
    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_token(jwt_token: str, installation_id: str) -> str:
    url = f"{GITHUB_API}/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json",
    }

    r = requests.post(url, headers=headers)
    r.raise_for_status()
    return r.json()["token"]


def github_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


# -----------------------------
# Git operations (NO PR logic)
# -----------------------------

def get_branch_sha(token: str, owner: str, repo: str, branch: str) -> str:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/ref/heads/{branch}"
    r = requests.get(url, headers=github_headers(token))
    r.raise_for_status()
    return r.json()["object"]["sha"]


def create_branch(
    token: str,
    owner: str,
    repo: str,
    new_branch: str,
    base_branch: str,
):
    base_sha = get_branch_sha(token, owner, repo, base_branch)

    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/refs"
    payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": base_sha,
    }

    r = requests.post(url, headers=github_headers(token), json=payload)

    # 422 = branch already exists (idempotent)
    if r.status_code not in (201, 422):
        r.raise_for_status()


def commit_files(
    token: str,
    owner: str,
    repo: str,
    branch: str,
    files: Dict[str, str],
    commit_message: str,
):
    """
    Commit/update files to an existing branch.

    files = {
        "path/to/file.txt": "file contents",
    }
    """

    for path, content in files.items():
        url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"

        encoded = base64.b64encode(content.encode()).decode()

        # Does file already exist?
        r = requests.get(url, headers=github_headers(token), params={"ref": branch})
        sha = r.json()["sha"] if r.status_code == 200 else None

        payload = {
            "message": commit_message,
            "content": encoded,
            "branch": branch,
        }

        if sha:
            payload["sha"] = sha

        r = requests.put(url, headers=github_headers(token), json=payload)
        r.raise_for_status()


# -----------------------------
# Pull Requests (NO git logic)
# -----------------------------

def create_pull_request(
    token: str,
    owner: str,
    repo: str,
    head: str,
    base: str,
    title: str,
    body: Optional[str] = None,
    draft: bool = True,
):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls"

    payload = {
        "title": title,
        "head": head,
        "base": base,
        "draft": draft,
    }

    if body:
        payload["body"] = body

    r = requests.post(url, headers=github_headers(token), json=payload)

    if r.status_code == 422:
        raise RuntimeError(f"PR validation failed: {r.json()}")

    r.raise_for_status()
    return r.json()


# -----------------------------
# Convenience helper (optional)
# -----------------------------

def get_app_token(
    *,
    app_id: str,
    installation_id: str,
    private_key_path: str,
) -> str:
    private_key = Path(private_key_path).read_text()
    jwt_token = generate_jwt(app_id, private_key)
    return get_installation_token(jwt_token, installation_id)
