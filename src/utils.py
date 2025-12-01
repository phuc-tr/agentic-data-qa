import os
import re
import json
import requests
from requests.exceptions import RequestException, Timeout
from dotenv import load_dotenv
load_dotenv()

class OpenRouterError(Exception):
    pass

def make_openrouter_request(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        #"model": "meta-llama/llama-3.3-70b-instruct:free",
        "model": "google/gemini-2.5-flash",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
    except Timeout:
        raise OpenRouterError("Request to OpenRouter timed out.")
    except RequestException as e:
        raise OpenRouterError(f"Network error: {e}")

    if not response.ok:
        # Try extracting API error message
        try:
            api_error = response.json().get("error")
        except Exception:
            api_error = response.text
        raise OpenRouterError(f"HTTP {response.status_code}: {api_error}")

    data = response.json()
    return data["choices"][0]["message"]["content"]

def extract_json(llm_response: str):
    """
    Extracts any JSON (array or object) from an LLM response.
    Prioritizes JSON inside ``` blocks, then scans full text.
    Returns dict or list.
    """
    
    # 1. Search inside fenced code blocks first
    code_block_matches = re.findall(r"```(?:json)?(.*?)```", llm_response, flags=re.DOTALL | re.IGNORECASE)
    for block in code_block_matches:
        block = block.strip()
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            pass

    # 2. Fallback: search for top-level objects or arrays
    json_candidates = re.findall(r"(\{[\s\S]*\}|\[[\s\S]*\])", llm_response)
    for candidate in json_candidates:
        candidate = candidate.strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    raise ValueError(f"No valid JSON found in LLM response. {llm_response}")
