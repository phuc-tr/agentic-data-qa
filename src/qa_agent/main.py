import subprocess
import json
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from qa_agent.langgraph_src.prompt import (
    GENERATE_CHECKS_PROMPT_TEMPLATE,
    GENERATE_GX_SUITE_TEMPLATE,
    GENERATE_GX_SUITE_TEMPLATE_SINGLE,
    GATER_PROMPT,
    UPDATE_CODE_PROMPT,
    CRAFT_PULL_REQUEST_PROMPT,
    FIX_ERROR_PROMPT
)
from qa_agent.langgraph_src.utils import get_latest_code, extract_python_code
from qa_agent.langgraph_src.validator import validate
from qa_agent.langgraph_src.github_utils import (
    create_branch,
    commit_files,
    create_pull_request,
    get_github_client,
)
from langgraph.graph import add_messages
from langchain.messages import SystemMessage, HumanMessage, ToolCall
from langchain_core.messages import BaseMessage
from langgraph.func import entrypoint, task
from langchain.agents import create_agent
from pydantic import BaseModel, Field
from pathlib import Path

from qa_agent.langgraph_src import sampler

# Load environment variables
env_path = Path.cwd() / ".env"
load_dotenv(env_path)

# Initialize models
model_coder = init_chat_model(model=getenv("CODER_MODEL", "gpt-5.2"))
model_writer = init_chat_model(model=getenv("WRITER_MODEL", "gpt-3.5-turbo"))

class GaterOutput(BaseModel):
    update_needed: bool = Field(description="Whether an update to the expectation suite is needed.")
    rationale: str = Field(description="Rationale for the decision.")

# -------------------- TASKS -------------------- #

@task
def propose_quality_checks(data_contract: str, data_profile: str) -> str:
    response = model_writer.invoke(
        GENERATE_CHECKS_PROMPT_TEMPLATE.format(contract=data_contract, profile=data_profile)
    )
    return response.content

@task
def generate_quality_code(checks: str, metadata:str, framework: str) -> str:
    response = model_coder.invoke(
        GENERATE_GX_SUITE_TEMPLATE.format(proposals=checks, metadata=metadata)
    )
    return response.content

@task
def generate_quality_code_single(contract: str) -> str:
    response = model_coder.invoke(
        GENERATE_GX_SUITE_TEMPLATE_SINGLE.format(contract=contract)
    )
    return response.content

@task
def gater(contract: str, latest_code: str, expectation_snippets: str) -> str:
    agent = create_agent(model_writer, response_format=GaterOutput)
    result = agent.invoke({
        "messages": GATER_PROMPT.format(
            contract=contract,
            latest_code=latest_code,
            expectation_snippets=expectation_snippets
        )
    })
    return result["structured_response"]

@task
def update_expectation_suite(contract: str, latest_code: str, expectation_snippets: str) -> str:
    response = model_coder.invoke(
        UPDATE_CODE_PROMPT.format(
            contract=contract,
            latest_code=latest_code,
            expectation_snippets=expectation_snippets
        )
    )
    return response.content

@task
def fix_errors_in_code(code: str, error_message: str) -> str:
    response = model_coder.invoke(
        FIX_ERROR_PROMPT.format(
            code=code,
            error_message=error_message
        )
    )
    return response.content

@task
def craft_pr_body(results: dict, old_code: str, new_code: str, data_contract: str) -> str:
    response = model_writer.invoke(
        CRAFT_PULL_REQUEST_PROMPT.format(
            results=json.dumps(results, indent=2),
            old_code=old_code,
            new_code=new_code,
            data_contract=data_contract
        )
    )
    return response.content

# -------------------- HELPER -------------------- #

def limit_dict_depth(data, max_depth: int = 4, current_depth: int = 0):
    """Limit dictionary depth to specified levels."""
    if current_depth >= max_depth:
        return str(data) if not isinstance(data, (dict, list)) else "..."
    
    if isinstance(data, dict):
        return {k: limit_dict_depth(v, max_depth, current_depth + 1) for k, v in data.items()}
    elif isinstance(data, list):
        return [limit_dict_depth(item, max_depth, current_depth + 1) for item in data]
    return data

def run_python_file(filepath: str, max_attempts: int = 5) -> str:
    """Run a Python file and return output or attempt fixes."""
    attempt = 0
    with open(filepath, "r") as f:
        code = f.read()

    while attempt < max_attempts:
        subprocess.run(["rm", "-rf", "gx"])
        proc = subprocess.run(["python", filepath], capture_output=True, text=True)
        if proc.returncode == 0:
            return code  # Successfully ran
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
    mode = params.get("mode", "default")
    owner, repo, dataset = params["owner"], params["repo"], params["dataset"]
    output_path, contract = params["output_path"], params["contract"]
    base_branch = params.get("base_branch", "main")
    run_id = params.get("run_id") or datetime.now().strftime("%Y%m%d%H%M%S")

    # Run sampler unless run_id is provided
    if not params.get("run_id"):
        Path('artifacts/samples').mkdir(parents=True, exist_ok=True)
        Path('artifacts/profiles').mkdir(parents=True, exist_ok=True)
        Path('artifacts/metadata').mkdir(parents=True, exist_ok=True)
        Path('artifacts/proposals').mkdir(parents=True, exist_ok=True)
        Path('artifacts/failing_examples').mkdir(parents=True, exist_ok=True)
        Path('artifacts/sandbox').mkdir(parents=True, exist_ok=True)

        sampler.sample(dataset=dataset, data_contract=contract, run_id=run_id)

    with open(contract) as f:
        data_contract = f.read()

    if mode == "single":
        code = generate_quality_code_single(contract=data_contract).result()
        code = extract_python_code(code)
        # 2. Craft PR and Push (Skipping validation/sampling)
        gh = get_github_client(getenv("GITHUB_APP_ID"), int(getenv("GITHUB_INSTALLATION_ID")), getenv("GITHUB_PRIVATE_KEY_PATH"))
        repo_obj = gh.get_repo(f"{owner}/{repo}")
        branch = f"bot/single-{run_id}"

        with open(output_path, "w") as f:
            f.write(code)
        
        create_branch(repo_obj, branch, base_branch=base_branch)
        commit_files(repo_obj, branch, {output_path: code}, "Single-agent update")
        
        pr_body = f"Automated Great Expectations suite generated from contract: {contract}"
        pr = create_pull_request(repo_obj, head=branch, base=base_branch, title="Auto-GX: Single Mode", body=pr_body, draft=True)
        print(f"✅ Pull request created: {pr.html_url}")
    else:
        if params.get("run_id"):
            # Skip generation, assume code is at output_path
            with open(output_path, "r") as f:
                updated_code = f.read()
            results = validate(run_id=run_id, dataset=dataset, data_contract=contract)

            gh = get_github_client(getenv("GITHUB_APP_ID"), int(getenv("GITHUB_INSTALLATION_ID")), getenv("GITHUB_PRIVATE_KEY_PATH"))
            repo = gh.get_repo(f"{owner}/{repo}")
            branch = f"bot/{run_id}"
            create_branch(repo, branch, base_branch=base_branch)
            commit_files(repo, branch, {
                "report.json": json.dumps(results, indent=2)
            }, "Validation results")
            pr_body = f"Validation results for run {run_id}"
            pr = create_pull_request(repo, head=branch, base=base_branch, title="Validation Report", body=pr_body, draft=True)
            print(f"✅ Pull request created: {pr.html_url}")
        else:
            # Load profiles & contracts
            with open(f"artifacts/profiles/{dataset}.{run_id}.json") as f:
                data_profile = json.load(f)
            with open(f"artifacts/metadata/{dataset}.schema_view.{run_id}.json") as f:
                metadata = f.read()

            # Generate quality checks and code
            checks = propose_quality_checks(data_contract, data_profile).result()
            with open(f"artifacts/proposals/{dataset}.{run_id}.json", "w") as f:
                f.write(checks)

            code = generate_quality_code(checks, metadata=metadata, framework="Great Expectations").result()

            # Load latest code and run gater
            latest_code = get_latest_code(
                filepath=f"expectations/{dataset}_suite.py",
                repo_name=f"{owner}/{repo}",
                branch=base_branch
            )

            gater_response = gater(
                contract=data_contract,
                latest_code=latest_code,
                expectation_snippets=code
            ).result()

            if gater_response.update_needed:
                print("✅ Update needed.")
                branch = f"bot/{run_id}"
                updated_code = update_expectation_suite(
                    contract=data_contract,
                    latest_code=latest_code,
                    expectation_snippets=code
                ).result()

                updated_code = extract_python_code(updated_code)

                with open(output_path, "w") as f:
                    f.write(updated_code)

                updated_code = run_python_file(output_path)  # Ensure code runs

                results = validate(run_id=run_id, dataset=dataset, data_contract=contract)
                pr_results = limit_dict_depth(results, max_depth=2)

                gh = get_github_client(getenv("GITHUB_APP_ID"), int(getenv("GITHUB_INSTALLATION_ID")), getenv("GITHUB_PRIVATE_KEY_PATH"))
                repo = gh.get_repo(f"{owner}/{repo}")

                create_branch(repo, branch, base_branch=base_branch)
                commit_files(repo, branch, {
                    output_path: updated_code,
                    "report.json": json.dumps(results, indent=2)
                }, "Automated update")

                pr_body = craft_pr_body(pr_results, latest_code, updated_code, data_contract).result()
                pr = create_pull_request(repo, head=branch, base=base_branch, title="WIP: Automated update", body=pr_body, draft=True)
                print(f"✅ Pull request created: {pr.html_url}")
            else:
                print("❌ No update needed.")
                print(gater_response.rationale)


import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=1)
    parser.add_argument("--repo", required=1)
    parser.add_argument("--dataset", required=1)
    parser.add_argument("--output_path", required=1)
    parser.add_argument("--contract", required=1)
    parser.add_argument("--base_branch", default='main')
    parser.add_argument("--mode", default='default')
    parser.add_argument("--run_id")
    args = parser.parse_args()

    workflow_entry.invoke({
        "owner": args.owner,
        "repo": args.repo,
        "dataset": args.dataset,
        "output_path": args.output_path,
        "contract": args.contract,
        "base_branch": args.base_branch,
        "mode": args.mode,
        "run_id": args.run_id,
    })

if __name__ == "__main__":
    main()