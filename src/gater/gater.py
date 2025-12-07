import json, re
from .prompt import PROMPT_TEMPLATE
from src import utils

confidence_threshold = 0.6


def extract_python_code(text: str):
    """Extract Python code block from an LLM response."""
    code_match = re.search(r"```(?:python)?\s*\n([\s\S]*?)\n?```", text, re.IGNORECASE)
    if code_match:
        return code_match.group(1).strip()
    if re.search(r'\b(def|class|import|from|if __name__|async|await)\b', text):
        return text.strip()
    return text.strip()


def main(run_id: str):
    dataset = "raddb"

    # ------------------------------------------------
    # Load proposals + runtime sandbox report
    # ------------------------------------------------
    with open(f"artifacts/proposals/{dataset}.{run_id}.json", "r") as f:
        proposals = json.load(f)
    with open(f"artifacts/sandbox/{dataset}.{run_id}.report.json", "r") as f:
        report = json.load(f)

    # ------------------------------------------------
    # 🔥 Compute acceptance-rate history directly
    # ------------------------------------------------
    # Example: calculate_acceptance_rates(repo, "2024-01-01")
    repo = utils.get_repo("phuc-tr/agent-data-qa")  # assuming you have this; adjust if necessary
    acceptance_rates = utils.calculate_acceptance_rates(repo, cutoff_date_str="2025-01-01")

    acceptance_index = {row["check_id"]: row for row in acceptance_rates}

    decisions = {}

    # ------------------------------------------------
    # Main decision loop
    # ------------------------------------------------
    for proposal in proposals:
        check_id = proposal["check_id"]
        likelihood = proposal.get("likelihood", 0)

        # ------------------------------------------------
        # 🔥 history = acceptance rate OR default 0.5
        # ------------------------------------------------
        if check_id in acceptance_index:
            total = acceptance_index[check_id]["total"]
            if total >= 2:
                history = acceptance_index[check_id]["acceptance_rate"]
            else:
                history = 0.5
        else:
            history = 0.5

        # ------------------------------------------------
        # Evidence from runtime sandbox report
        # ------------------------------------------------
        matched_results = [
            res for res in report["results"]
            if res["expectation_config"]["meta"].get("check_id") == check_id
        ]

        if matched_results:
            evidence = matched_results[0]["result"].get("unexpected_percent", 0)
        else:
            evidence = 100  # worst case

        evidence = evidence / 100.0

        # ------------------------------------------------
        # Confidence score
        # ------------------------------------------------
        confidence = 0.4 * likelihood + 0.4 * evidence + 0.2 * history

        decisions[check_id] = {
            "likelihood": likelihood,
            "evidence": evidence,
            "history": history,
            "confidence": confidence,
            "go": confidence >= confidence_threshold
        }

    # ------------------------------------------------
    # Save decisions
    # ------------------------------------------------
    output_path = f"artifacts/decisions/{dataset}.{run_id}.decision.json"
    with open(output_path, "w") as f:
        json.dump(decisions, f, indent=2)
    print(f"✅ Decisions saved to {output_path}")

    # ------------------------------------------------
    # Keep only "go" proposals
    # ------------------------------------------------
    filtered_proposals = {
        "proposals": [p for p in proposals if decisions[p["check_id"]]["go"]]
    }

    if not filtered_proposals["proposals"]:
        print("No proposals passed the gating criteria.")
        return 0

    # ------------------------------------------------
    # Apply LLM filtering to expectation suite
    # ------------------------------------------------
    with open(f"expectations/{dataset}_suite.py", "r") as f:
        expectation_suite = f.read()

    prompt = PROMPT_TEMPLATE.format(
        decisions_json=json.dumps(decisions, indent=2),
        expectation_snippets=expectation_suite
    )

    response = utils.make_openrouter_request(prompt)
    suite = extract_python_code(response)

    with open(f"expectations/{dataset}_suite.py", "w") as f:
        f.write(suite)

    print(f"✅ Filtered expectation suite saved to expectations/{dataset}_suite.py")
    return 1


if __name__ == "__main__":
    main("20251202185330")
