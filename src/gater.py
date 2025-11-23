import json

history = 0.5  # Placeholder for historical performance metric
confidence_threshold = 0.5

def main(run_id: str):
    dataset = "raddb"

    with open(f"artifacts/proposals/{dataset}.{run_id}.json", "r") as f:
        proposals = json.load(f)
    with open(f"artifacts/sandbox/{dataset}.{run_id}.report.json", "r") as f:
        report = json.load(f)

    decisions = {}
    
    for proposal in proposals["proposals"]:
        likelihood = proposal.get("likelihood", 0)
        check_id = proposal["check_id"]

        matched_results = [res for res in report["results"] if res["expectation_config"]["meta"].get("check_id") == check_id]
        
        if matched_results:
            evidence = matched_results[0].get("result").get("unexpected_percent")
            if  evidence is None:
                evidence = 0
        else:
            evidence = 1.0  # No matching result, assume worst case
        evidence = evidence / 100
        confidence = 0.4 * likelihood + 0.4 * evidence + 0.2 * history
        decisions[check_id] = {
            "likelihood": likelihood,
            "evidence": evidence,
            "confidence": confidence,
            "go": confidence >= confidence_threshold
        }
        # print(f"Check {check_id}: likelihood={likelihood:.2f}, evidence={evidence:.2f}, confidence={confidence:.2f}, go={decisions[check_id]['go']}")    

    output_path = f"artifacts/decisions/{dataset}.{run_id}.decision.json"
    with open(output_path, "w") as f:
        json.dump(decisions, f, indent=2)
    print(f"✅ Decisions saved to {output_path}")
    

if __name__ == "__main__":
    main("20251123115408")