import os
import json
import re
from .prompt import PROMPT_TEMPLATE
from .post_process import post_process_checks
from src import utils

def strip_to_json(text: str):
    """Extract valid JSON object from a text blob."""
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            return text
    return text

def main(run_id: str):
    dataset = "raddb"

    with open(f"artifacts/metadata/{dataset}.schema_view.{run_id}.json", "r") as f:
        schema_view = json.load(f)
    with open(f"artifacts/profiles/{dataset}.{run_id}.json", "r") as f:
        profile = json.load(f)
    with open(f"contracts/contract.{dataset}.yaml", "r") as f:
        contract = f.read()

    # Fill in the prompt
    prompt = PROMPT_TEMPLATE.format(
        contract=contract.strip(),
        schema=json.dumps(schema_view, indent=2),
        profile=json.dumps(profile, indent=2),
    )
    
    # Make request to LLM
    response = utils.make_openrouter_request(prompt)

    # Extract JSON
    json_data = strip_to_json(response)
    json_data["proposals"] = post_process_checks(json_data["proposals"])

    #TODO: Validate output: column exists, params valid (min ≤ max), types compatible.

    # Save output
    output_path = f"artifacts/proposals/{dataset}.{run_id}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        if json_data:
            json.dump(json_data, f, indent=2)
        else:
            f.write(response.text)

    print(f"✅ Generated checks saved to {output_path}")

    import yaml
    contract_yaml = yaml.safe_load(contract)
    contract_rules = {q["rule"] for q in contract_yaml.get("schema")[0].get("quality", [])}
    proposed_rules = {p["origin"]["rule"] for p in json_data["proposals"] if "rule" in p.get("origin", {})}
    covered_rules = contract_rules.intersection(proposed_rules)
    coverage = len(covered_rules) / len(contract_rules) if contract_rules else 1.0
    print(f"✅ Coverage report: {len(covered_rules)}/{len(contract_rules)} rules covered ({coverage:.2%})")
    for rule in contract_rules:
        status = "✅" if rule in proposed_rules else "❌"
        print(f"  {status} {rule}")