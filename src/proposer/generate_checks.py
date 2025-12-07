import os
import json
from .prompt import PROMPT_TEMPLATE
from .post_process import post_process_checks
from src import utils


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
        # schema=json.dumps(schema_view, indent=2),
        profile=json.dumps(profile, indent=2),
    )
    
    # Make request to LLM
    response = utils.make_openrouter_request(prompt)

    # Extract JSON
    json_data = utils.extract_json(response)

    json_data = post_process_checks(json_data)

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
