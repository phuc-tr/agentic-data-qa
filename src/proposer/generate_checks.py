import os
import json
import re
from dotenv import load_dotenv
from google import genai
from prompt import PROMPT_TEMPLATE
from post_process import post_process_checks

def strip_to_json(text: str):
    """Extract valid JSON object from a text blob."""
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            return text
    return text


def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    dataset = "raddb"
    run_id = "20251104205844"

    # Load input files
    # print current workdir

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

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Generate model output
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    # Extract JSON
    json_data = strip_to_json(response.text)
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


if __name__ == "__main__":
    main()
