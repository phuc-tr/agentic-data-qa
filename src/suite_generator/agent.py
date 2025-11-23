import os
import json
import re
from dotenv import load_dotenv
from src import utils
from .prompt import PROMPT_TEMPLATE

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

    suite = extract_python_code(response)

    output_path = f"expectations/{dataset}_suite.py"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(suite)
    print(f"✅ Generated expectation suite saved to {output_path}")

if __name__ == "__main__":
    main()