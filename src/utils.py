from base64 import b64decode
import os
import re
import json
import re
from datetime import datetime, timezone
from collections import defaultdict
import requests
from requests.exceptions import RequestException, Timeout
from dotenv import load_dotenv
load_dotenv()

class OpenRouterError(Exception):
    pass

def make_openrouter_request(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        #"model": "google/gemini-2.5-flash",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
    except Timeout:
        raise OpenRouterError("Request to OpenRouter timed out.")
    except RequestException as e:
        raise OpenRouterError(f"Network error: {e}")

    if not response.ok:
        # Try extracting API error message
        try:
            api_error = response.json().get("error")
        except Exception:
            api_error = response.text
        raise OpenRouterError(f"HTTP {response.status_code}: {api_error}")

    data = response.json()
    return data["choices"][0]["message"]["content"]

def extract_json(llm_response: str):
    """
    Extracts any JSON (array or object) from an LLM response.
    Prioritizes JSON inside ``` blocks, then scans full text.
    Returns dict or list.
    """
    
    # 1. Search inside fenced code blocks first
    code_block_matches = re.findall(r"```(?:json)?(.*?)```", llm_response, flags=re.DOTALL | re.IGNORECASE)
    for block in code_block_matches:
        block = block.strip()
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            pass

    # 2. Fallback: search for top-level objects or arrays
    json_candidates = re.findall(r"(\{[\s\S]*\}|\[[\s\S]*\])", llm_response)
    for candidate in json_candidates:
        candidate = candidate.strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    raise ValueError(f"No valid JSON found in LLM response. {llm_response}")

def extract_python_code(text: str):
    """Extract Python code block from an LLM response."""
    code_match = re.search(r"```(?:python)?\s*\n([\s\S]*?)\n?```", text, re.IGNORECASE)
    if code_match:
        return code_match.group(1).strip()
    if re.search(r'\b(def|class|import|from|if __name__|async|await)\b', text):
        return text.strip()
    return text.strip()

def get_data_contract(filepath="contracts/contract.raddb.yaml"):
    """
    Load data contract YAML file and return as dict.
    """
    import yaml

    with open(filepath, "r") as f:
        contract = yaml.safe_load(f)

    return contract

import sqlalchemy
import pandas as pd
import ydata_profiling

def get_data_profile(filepath="contracts/contract.raddb.yaml", only_alert=True):
    # Get credentials from data contract
    contract = get_data_contract(filepath)
    server = contract.get("servers").get("mysql")
    username = server.get("username")
    password = server.get("password")
    host = server.get("host")
    port = server.get("port")
    database = server.get("database")
    uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    engine = sqlalchemy.create_engine(uri)
    query = "SELECT * FROM radacct ORDER BY acctstarttime DESC LIMIT 100;"
    df = pd.read_sql(query, engine)
    profile = ydata_profiling.ProfileReport(df, title="YData Profiling Report", minimal=True)
    json_data = json.loads(profile.to_json())

    if only_alert:
        return json_data['alerts']
    return json_data


from github import Github
import os

def get_latest_expectation_suite(filepath="expectations/raddb_suite.py"):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GITHUB_TOKEN environment variable")

    gh = Github(token)
    repo = gh.get_repo("phuc-tr/agentic-data-qa")
    try:
        contents = repo.get_contents(filepath, ref="main")
    except Exception:
        return ""
    file_content = b64decode(contents.content).decode("utf-8")
    return file_content

def calculate_acceptance_rates(repo, cutoff_date_str, filepath="expectations/raddb_suite.py"):
    """
    Compute acceptance rate per check_id for PRs created after cutoff_date.

    Args:
        repo: PyGithub repository object.
        cutoff_date_str: "YYYY-MM-DD" string.
        filepath: path to the file to inspect inside each PR.

    Returns:
        List of dicts with:
            - check_id
            - total
            - accepted
            - acceptance_rate
    """

    # Convert cutoff date string to datetime
    cutoff_dt = datetime.strptime(cutoff_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    # Regex to extract check_id="..."
    CHECK_ID_RE = re.compile(r'check_id"\s*:\s*"([^"]+)"')

    # Collect raw rows
    results = []

    # Pull all PRs, open and closed
    all_prs = repo.get_pulls(state="all")

    for pr in all_prs:
        # Skip PRs older than cutoff date
        if pr.created_at < cutoff_dt:
            continue

        # Extract file content
        content = get_file_content_from_pr(pr, filepath)
        if not content:
            continue

        # Find all check IDs
        check_ids = CHECK_ID_RE.findall(content)

        # Store rows
        for cid in check_ids:
            results.append({
                "pr_id": pr.number,
                "check_id": cid,
                "accepted": pr.merged is True
            })

    # Compute acceptance stats
    stats = defaultdict(lambda: {"total": 0, "accepted": 0})

    for row in results:
        cid = row["check_id"]
        stats[cid]["total"] += 1
        if row["accepted"]:
            stats[cid]["accepted"] += 1

    # Convert to list of summary dicts
    acceptance_rates = []
    for cid, s in stats.items():
        acceptance_rates.append({
            "check_id": cid,
            "total": s["total"],
            "accepted": s["accepted"],
            "acceptance_rate": s["accepted"] / s["total"] if s["total"] else 0.0
        })

    return acceptance_rates


def get_repo(repo_name):
    """
    Return a PyGithub repo object.
    Must set GITHUB_TOKEN and REPO_NAME in environment variables, OR replace 
    these lines with your own values directly.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GITHUB_TOKEN environment variable")

    gh = Github(token)
    return gh.get_repo(repo_name)

def get_file_content_from_pr(pr, filename="expectations/raddb_suite.py"):
    token = os.getenv("GITHUB_TOKEN")
    for file in pr.get_files():
        if file.filename == filename:
            headers = {"Authorization": f"token {token}"}
            response = requests.get(file.contents_url, headers=headers)
            response.raise_for_status()
            content_json = response.json()
            content = b64decode(content_json["content"]).decode("utf-8")
            return content
    return None
