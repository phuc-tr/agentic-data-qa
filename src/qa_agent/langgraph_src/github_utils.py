from pathlib import Path
from typing import Dict, Optional
from github import Github, Auth, GithubException

# -----------------------------
# Auth & Initialization
# -----------------------------

def get_github_client(app_id: str, installation_id: int, private_key_path: str) -> Github:
    """
    Initializes the Github client using App Authentication.
    The SDK handles JWT signing and installation token retrieval.
    """
    private_key = Path(private_key_path).read_text()
    
    # 1. Create Auth object for the App
    auth = Auth.AppAuth(app_id, private_key)
    
    # 2. Scope the auth to the specific installation
    installation_auth = auth.get_installation_auth(installation_id)
    
    # 3. Return the authenticated client
    return Github(auth=installation_auth)


# -----------------------------
# Git Operations
# -----------------------------

def create_branch(repo, new_branch: str, base_branch: str):
    """Creates a branch if it doesn't exist."""
    try:
        base_ref = repo.get_git_ref(f"heads/{base_branch}")
        repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=base_ref.object.sha)
    except GithubException as e:
        # 422 indicates the branch already exists
        if e.status != 422:
            raise


def commit_files(repo, branch: str, files: Dict[str, str], commit_message: str):
    """
    Commit/update files. The SDK handles checking for existing SHAs 
    and base64 encoding automatically.
    """
    for path, content in files.items():
        try:
            # Check if file exists to get its SHA for an update
            contents = repo.get_contents(path, ref=branch)
            repo.update_file(
                path=path,
                message=commit_message,
                content=content,
                sha=contents.sha,
                branch=branch
            )
        except GithubException as e:
            if e.status == 404:
                # File does not exist, create it
                repo.create_file(
                    path=path,
                    message=commit_message,
                    content=content,
                    branch=branch
                )
            else:
                raise


# -----------------------------
# Pull Requests
# -----------------------------

def create_pull_request(
    repo,
    head: str,
    base: str,
    title: str,
    body: Optional[str] = None,
    draft: bool = True,
):
    return repo.create_pull(
        title=title,
        body=body or "",
        base=base,
        head=head,
        draft=draft
    )
