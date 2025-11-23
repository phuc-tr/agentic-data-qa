import json
def main(run_id: str):
    dataset = "rabddb"

    # Open 
    # artifacts/proposals/<dataset>.<run_id>.json. 
    # artifacts/sandbox/<dataset>.<run_id>.report.json (evidence). 
    with open(f"artifacts/proposals/{dataset}.{run_id}.json", "r") as f:
        proposals = json.load(f)
    with open(f"artifacts/sandbox/{dataset}.{run_id}.report.json", "r") as f:
        report = json.load(f)

    # Simple gating logic: 
    # Calculate confidence score 
    # confidence = 0.4·likelihood + 0.4·evidence
    # evidence is unexpected_percent in report.
    
    for proposal in proposals["proposals"]:
        likelihood = proposal.get("likelihood", 0)
        check_id = proposal["check_id"]

        # Find corresponding result in report
        result = next((r for r in report["results"] if r["expectation_config"]["kwargs"]["column"] in check_id), None)
        if result:
            unexpected_percent = result["result"].get("unexpected_percent", 1.0)
        else:
            unexpected_percent = 1.0  # No evidence, assume worst

        evidence = 1.0 - unexpected_percent
        confidence = 0.4 * likelihood + 0.4 * evidence
        proposal["confidence"] = confidence