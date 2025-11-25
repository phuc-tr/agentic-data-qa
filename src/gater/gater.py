import json, re
from .prompt import PROMPT_TEMPLATE
from src import utils

history = 0.5  # Placeholder for historical performance metric
confidence_threshold = 0.6

def extract_python_code(text: str):
    """Extract Python code from a response text.

    This looks for a fenced code block (```python or ```) and returns the
    contained code without the fence markers. If no fenced block is found,
    it heuristically returns the original text if it looks like Python,
    otherwise returns the stripped original text.
    """
    # Match ```python\n...``` or ```\n...``` (non-greedy)
    code_match = re.search(r"```(?:python)?\s*\n([\s\S]*?)\n?```", text, re.IGNORECASE)
    if code_match:
        return code_match.group(1).strip()

    # Fallback heuristic: if text contains common Python tokens, return it
    if re.search(r'\b(def|class|import|from|if __name__|async|await)\b', text):
        return text.strip()

    return text.strip()

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

    # Filter checks to keep only those marked as 'go'
    filtered_proposals = {
        "proposals": [p for p in proposals["proposals"] if decisions[p["check_id"]]["go"]]
    }

    if len(filtered_proposals["proposals"]) == 0:
        print("No proposals passed the gating criteria.")
        return 0
    
    # Use prompt template to filter expectation snippets
    with open(f"expectations/{dataset}_suite.py", "r") as f:
        expectation_suite = f.read()

    prompt = PROMPT_TEMPLATE.format(
        decisions_json=json.dumps(decisions, indent=2),
        expectation_snippets=expectation_suite)
    
    response = utils.make_openrouter_request(prompt)
    suite = extract_python_code(response)
    with open(f"expectations/{dataset}_suite.py", "w") as f:
        f.write(suite)
    print(f"✅ Filtered expectation suite saved to expectations/{dataset}_suite.py")
    return 1
    

if __name__ == "__main__":
    main("20251125084533")