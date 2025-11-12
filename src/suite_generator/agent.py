import os
import json
import re
from dotenv import load_dotenv
from google import genai
from prompt import PROMPT_TEMPLATE

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

    with open(f"artifacts/proposals/{dataset}.{run_id}.json", "r") as f:
        proposals = json.load(f)
    
    prompt = PROMPT_TEMPLATE.format(
        proposals=json.dumps(proposals, indent=2)
    )

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Generate model output
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    suite = strip_to_json(response.text)

    with open(f"expectations/{dataset}_suite.json", "w") as f:
        json.dump(suite, f, indent=2)

if __name__ == "__main__":
    main()