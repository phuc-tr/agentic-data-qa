import argparse
import json
import os
import shutil
import subprocess


def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def build_pr_body(dataset: str, run_id: str):
    # Load proposals, decisions and compose PR body sections
    proposals_path = f"artifacts/proposals/{dataset}.{run_id}.json"
    decisions_path = f"artifacts/decisions/{dataset}.{run_id}.decision.json"
    report_path = f"artifacts/sandbox/{dataset}.{run_id}.report.json"
    failing_path = f"artifacts/failing_examples/{dataset}.{run_id}.csv"

    proposals = {}
    decisions = {}
    try:
        with open(proposals_path, "r") as f:
            proposals = json.load(f)
    except Exception:
        proposals = {}

    try:
        with open(decisions_path, "r") as f:
            decisions = json.load(f)
    except Exception:
        decisions = {}

    why_now = (
        f"Automated QA run for dataset `{dataset}` (run_id `{run_id}`) producing checks and proposals based on contracts and profiles."
    )

    checks_lines = []
    evidence_lines = []
    confidence_lines = []

    for p in proposals.get("proposals", []):
        cid = p.get("check_id")
        if not cid:
            continue
        decisions_entry = decisions.get(cid, {})
        go = decisions_entry.get("go")
        if go:
            checks_lines.append(f"- {cid}: {p.get('rationale','')}")
            evidence_lines.append(f"- {cid}: evidence={decisions_entry.get('evidence')}")
            confidence_lines.append(f"- {cid}: confidence={decisions_entry.get('confidence')}")

    if not checks_lines:
        checks_text = "No checks selected to apply."
    else:
        checks_text = "\n".join(checks_lines)

    evidence_text = "\n".join(evidence_lines) if evidence_lines else "No evidence available."
    confidence_text = "\n".join(confidence_lines) if confidence_lines else "No confidence values available."

    rollback = (
        "If these checks cause regressions, revert this PR or remove/disable the failing expectations. "
        "You can also roll back by reverting the commit or re-running the pipeline with previous expectations."
    )

    metadata = (
        f"- dataset: {dataset}\n- run_id: {run_id}\n- proposals: {proposals_path}\n- decisions: {decisions_path}\n- report: {report_path}\n- failing_examples: {failing_path}"
    )

    body = (
        f"Why now:\n{why_now}\n\n"
        f"Checks:\n{checks_text}\n\n"
        f"Evidence:\n{evidence_text}\n\n"
        f"Rollback:\n{rollback}\n\n"
        f"Confidence:\n{confidence_text}\n\n"
        f"Metadata:\n{metadata}\n"
    )

    return body


def main(run_id):
    dataset = "raddb"

    branch = f"pr/{dataset}/{run_id}"

    # Create branch
    run(f"git branch -D {branch} || true")
    run(f"git checkout -b {branch}")

    # Prepare files to commit
    src_suite = "expectations/raddb_suite.py"
    src_report = f"artifacts/sandbox/{dataset}.{run_id}.report.json"
    dest_dir = "reports"
    os.makedirs(dest_dir, exist_ok=True)
    dest_report = os.path.join(dest_dir, f"{run_id}_{dataset}_sandbox_report.json")

    if os.path.exists(src_report):
        shutil.copyfile(src_report, dest_report)
        print(f"Copied report to {dest_report}")
    else:
        print(f"Warning: source report not found at {src_report}")

    failing_src = f"artifacts/failing_examples/{dataset}.{run_id}.csv"
    if not os.path.exists(failing_src):
        print(f"Warning: failing examples not found at {failing_src}")

    # Add files to git
    files_to_add = []
    if os.path.exists(src_suite):
        files_to_add.append(src_suite)
    else:
        print(f"Warning: suite file not found at {src_suite}")
    if os.path.exists(dest_report):
        files_to_add.append(dest_report)
    if os.path.exists(failing_src):
        files_to_add.append(failing_src)

    if not files_to_add:
        print("No files found to add to the PR. Exiting.")
        run("git checkout main")
        return

    for fp in files_to_add:
        run(f"git add {fp}")

    commit_msg = f"chore: add QA report and failing examples for {dataset} {run_id}"
    run(f"git commit -m \"{commit_msg}\"")

    run(f"git push -u origin {branch}")

    body = build_pr_body(dataset, run_id)

    title = f"Data QA: {dataset} — run {run_id}"
    # Create PR (draft) with gh
    # Use temporary file for body to avoid shell escaping issues
    body_file = ".pr_body_temp"
    with open(body_file, "w") as f:
        f.write(body)
    try:
        run(f'gh pr create --base main --head {branch} --title "{title}" --body-file {body_file} --draft')
    finally:
        if os.path.exists(body_file):
            os.remove(body_file)

    # Switch back to main
    run("git checkout main")
