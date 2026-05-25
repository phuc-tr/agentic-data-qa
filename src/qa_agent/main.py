import subprocess
import json
import yaml
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from qa_agent.langgraph_src.prompt import (
    GENERATE_GX_UNRESOLVED_PROMPT,
    FIX_ERROR_PROMPT,
    CRAFT_PULL_REQUEST_PROMPT,
)
from qa_agent.langgraph_src.utils import extract_python_code
from qa_agent.langgraph_src.validator import validate
from qa_agent.langgraph_src.contract_parser import (
    build_base_suite_from_cli,
    parse_cli_coverage,
    extract_unresolved_rules,
    build_llm_fragment,
)
from qa_agent.langgraph_src.github_utils import (
    create_branch,
    commit_files,
    create_pull_request,
    get_github_client,
)
from langgraph.func import entrypoint, task
from pathlib import Path

from qa_agent.langgraph_src import sampler

# Load environment variables
env_path = Path.cwd() / ".env"
load_dotenv(env_path)

# Initialize models
model_coder = init_chat_model(model=getenv("CODER_MODEL", "gpt-5.2"))
model_writer = init_chat_model(model=getenv("WRITER_MODEL", "gpt-3.5-turbo"))

# -------------------- TASKS -------------------- #

@task
def generate_gx_for_unresolved(fragment: str, metadata: str) -> str:
    response = model_coder.invoke(
        GENERATE_GX_UNRESOLVED_PROMPT.format(fragment=fragment, metadata=metadata)
    )
    return response.content

@task
def fix_errors_in_code(code: str, error_message: str) -> str:
    response = model_coder.invoke(
        FIX_ERROR_PROMPT.format(code=code, error_message=error_message)
    )
    return response.content

@task
def craft_pr_body(results: dict, old_code: str, new_code: str, data_contract: str) -> str:
    response = model_writer.invoke(
        _truncate(CRAFT_PULL_REQUEST_PROMPT.format(
            results=json.dumps(results, indent=2),
            old_code=old_code,
            new_code=new_code,
            data_contract=data_contract,
        ))
    )
    return response.content

# -------------------- HELPERS -------------------- #

GX_SUITE_NAME = "expectation_suite"


def _read_gx_suite_json(suite_name: str = GX_SUITE_NAME) -> str:
    with open(f"gx/expectations/{suite_name}.json") as f:
        return f.read()


def _suite_json_path(output_path: str) -> str:
    return output_path.replace(".py", ".json")


def _truncate(text: str, max_chars: int = 3000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n... [truncated {len(text) - max_chars} chars]"


def limit_dict_depth(data, max_depth: int = 4, current_depth: int = 0):
    if current_depth >= max_depth:
        return str(data) if not isinstance(data, (dict, list)) else "..."
    if isinstance(data, dict):
        return {k: limit_dict_depth(v, max_depth, current_depth + 1) for k, v in data.items()}
    elif isinstance(data, list):
        return [limit_dict_depth(item, max_depth, current_depth + 1) for item in data]
    return data


def run_python_file(filepath: str, max_attempts: int = 5, reset_gx: bool = True) -> str:
    """Run a Python file; retry with LLM error-fixing on failure."""
    attempt = 0
    with open(filepath) as f:
        code = f.read()

    while attempt < max_attempts:
        if reset_gx:
            subprocess.run(["rm", "-rf", "gx"])
        proc = subprocess.run(["python", filepath], capture_output=True, text=True)
        if proc.returncode == 0:
            return code
        print(f"❌ Error in generated code. Attempt {attempt + 1}/{max_attempts}")
        print(proc.stderr)
        code = fix_errors_in_code(code, proc.stderr).result()
        code = extract_python_code(code)
        with open(filepath, "w") as f:
            f.write(code)
        attempt += 1

    raise RuntimeError("Failed to run generated code after multiple attempts.")

# -------------------- MAIN ENTRYPOINT -------------------- #

@entrypoint()
def workflow_entry(params: dict):
    owner, repo, dataset = params["owner"], params["repo"], params["dataset"]
    output_path, contract = params["output_path"], params["contract"]
    base_branch = params.get("base_branch", "main")
    run_id = params.get("run_id") or datetime.now().strftime("%Y%m%d%H%M%S")

    # Run sampler unless a run_id was supplied (re-use existing artifacts)
    if not params.get("run_id"):
        for d in ["samples", "profiles", "metadata", "proposals", "failing_examples", "sandbox"]:
            Path(f"artifacts/{d}").mkdir(parents=True, exist_ok=True)
        sampler.sample(dataset=dataset, data_contract=contract, run_id=run_id)

    with open(contract) as f:
        data_contract = f.read()
        contract_dict = yaml.safe_load(data_contract)

    # Load metadata if available
    metadata_path = f"artifacts/metadata/{dataset}.schema_view.{run_id}.json"
    try:
        with open(metadata_path) as f:
            metadata = f.read()
    except FileNotFoundError:
        metadata = "{}"

    # ── Stage 1: datacontract CLI export (schema-level checks) ──────────────
    print("🔧 Stage 1: datacontract CLI export...")
    subprocess.run(["rm", "-rf", "gx"])
    cli_count = build_base_suite_from_cli(contract, suite_name=GX_SUITE_NAME)
    print(f"✅ Stage 1 complete — {cli_count} rule(s) handled by CLI.")

    # ── Stage 2: classify — find rules the CLI could not handle ─────────────
    print("🔍 Stage 2: classifying unresolved rules...")
    cli_suite = json.loads(_read_gx_suite_json())
    cli_coverage = parse_cli_coverage(cli_suite)
    unresolved = extract_unresolved_rules(contract_dict, cli_coverage=cli_coverage)
    if unresolved:
        print(f"  Found {len(unresolved)} unresolved rule(s): "
              + ", ".join(f"{r['field']}({r['rule'].get('type','?')})" for r in unresolved))
    else:
        print("  No unresolved rules — skipping LLM stage.")

    # ── Stage 3: LLM for unresolved rules only ──────────────────────────────
    llm_path = None
    llm_code = None
    if unresolved:
        print("🤖 Stage 3: LLM generating expectations for unresolved rules...")
        llm_fragment = build_llm_fragment(unresolved)
        llm_code = generate_gx_for_unresolved(llm_fragment, metadata).result()
        llm_code = extract_python_code(llm_code)

        llm_path = output_path.replace(".py", "_llm.py")
        with open(llm_path, "w") as f:
            f.write(llm_code)

        # reset_gx=False: preserve the CLI-generated suite from Stage 1
        run_python_file(llm_path, max_attempts=5, reset_gx=False)
        print("✅ Stage 3 complete.")

    # ── Stage 4: validate + commit ───────────────────────────────────────────
    print("📊 Stage 4: validating and committing...")
    suite_json = _read_gx_suite_json()
    local_suite_path = _suite_json_path(output_path)
    Path(local_suite_path).parent.mkdir(parents=True, exist_ok=True)
    Path(local_suite_path).write_text(suite_json)
    results = validate(run_id=run_id, dataset=dataset, data_contract=contract)
    pr_results = limit_dict_depth(results, max_depth=2)

    gh = get_github_client(
        getenv("GITHUB_APP_ID"),
        int(getenv("GITHUB_INSTALLATION_ID")),
        getenv("GITHUB_PRIVATE_KEY_PATH"),
    )
    repo_obj = gh.get_repo(f"{owner}/{repo}")
    branch = f"bot/{run_id}"

    files_to_commit = {
        _suite_json_path(output_path): suite_json,
        "report.json": json.dumps(results, indent=2),
    }
    if llm_path and llm_code:
        with open(llm_path) as f:
            files_to_commit[llm_path] = f.read()

    create_branch(repo_obj, branch, base_branch=base_branch)
    commit_files(repo_obj, branch, files_to_commit, "Automated update")

    pr_body = craft_pr_body(pr_results, "", suite_json, data_contract).result()
    pr = create_pull_request(
        repo_obj, head=branch, base=base_branch,
        title="WIP: Automated update", body=pr_body, draft=True,
    )
    print(f"✅ Pull request created: {pr.html_url}")


import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--base_branch", default="main")
    parser.add_argument("--run_id")
    args = parser.parse_args()

    workflow_entry.invoke({
        "owner": args.owner,
        "repo": args.repo,
        "dataset": args.dataset,
        "output_path": args.output_path,
        "contract": args.contract,
        "base_branch": args.base_branch,
        "run_id": args.run_id,
    })

if __name__ == "__main__":
    main()
