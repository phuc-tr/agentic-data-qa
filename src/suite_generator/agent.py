import os
import json
import re
from dotenv import load_dotenv
from src import utils
from .prompt import PROMPT_TEMPLATE

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
    # Load environment variables (also loaded inside utils but safe to call)
    load_dotenv()
    
    dataset = "raddb"

    with open(f"artifacts/proposals/{dataset}.{run_id}.json", "r") as f:
        proposals = json.load(f)
    
    prompt = PROMPT_TEMPLATE.format(
        proposals=json.dumps(proposals, indent=2)
    )

    # Make request via shared utility (OpenRouter)
    response = utils.make_openrouter_request(prompt)

    suite = strip_to_json(response)

    output_path = f"expectations/{dataset}_suite.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        if isinstance(suite, (dict, list)):
            json.dump(suite, f, indent=2)
        else:
            f.write(suite)
    print(f"✅ Generated expectation suite saved to {output_path}")

if __name__ == "__main__":
    main()