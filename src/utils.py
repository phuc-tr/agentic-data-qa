import os
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
        "model": "meta-llama/llama-3.3-70b-instruct:free",
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
