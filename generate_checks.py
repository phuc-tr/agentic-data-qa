import json
import os
import re
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

def strip_to_json(text):
    """Strip LLM response to get valid JSON."""
    # Find content between the first { and last }
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        potential_json = json_match.group(1)
        try:
            # Validate and format the JSON
            return json.loads(potential_json)
        except json.JSONDecodeError:
            return None
    return None

dataset = 'raddb'
run_id = '20251104205844'

with open(f'artifacts/metadata/{dataset}.schema_view.{run_id}.json', 'r') as f:
    schema_view = json.load(f)
with open(f'artifacts/profiles/{dataset}.{run_id}.json', 'r') as f:
    profile = json.load(f)
with open(f'contracts/contract.{dataset}.yaml', 'r') as f:
    contract = f.read()

example = """
Example output: 
{
  "dataset": "orders",
  "proposals": [
   {"check_id":"orders:unique:order_id","type":"unique","column":"order_id","params":{},"rationale":"Contract says unique; distinct_ratio=1.0","signals":{"distinct_ratio":1.0},"likelihood":0.80,"origin":{"from_contract":true}},
   {"check_id":"orders:domain:country","type":"domain","column":"country","params":{"allowed_set":["US","DE","IT","FR"]},"rationale":"Contract domain; observed 38 OOV values","signals":{"oov_rate":0.235},"likelihood":0.73,"origin":{"from_contract":true}},
   {"check_id":"orders:freshness:created_at","type":"freshness","column":"created_at","params":{"max_delay_min":30},"rationale":"SLA 30m; observed 69m","signals":{"freshness_minutes":69},"likelihood":0.88,"origin":{"from_contract":true}},
   {"check_id":"orders:range:amount","type":"range","column":"amount","params":{"min_value":0,"max_value":890},"rationale":"Use p99=890 as upper bound; long tail to 12840","signals":{"p99":890,"max":12840},"likelihood":0.55,"origin":{"from_profile":true}}
  ]
}
"""

# Generate checks with Gemini
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"""
You are a data quality engineer. You need to:

Read the data contract and the latest profile, then produce up to 10 well-parameterized checks (NOT NULL, UNIQUE, RANGE, IN-SET, FK, FRESHNESS).
Each check includes: params, rationale, signals, and a likelihood (risk/utility) score.

Detailed steps:

Identify gaps & anomalies from contract + profile (e.g., required columns with nulls, IDs with duplicates, out-of-range values, OOV categories, staleness, FK mismatches).
Map issues to check types: NOT NULL, UNIQUE, RANGE, IN-SET/DOMAIN, FRESHNESS, FK.
Parameterize checks: prefer contract values; if absent, use profile stats (e.g., RANGE min=p01, max=p99; FRESHNESS from SLA; IN-SET from contract domain).
Compute a likelihood score (0–1) per proposal from profile signals (e.g., null_rate, dup_rate, oov_rate, freshness delay).

Example:
{example}

Contract:
{contract}
Schema:
{json.dumps(schema_view, indent=2)}
Profile:
{json.dumps(profile, indent=2)}
Output the checks as a JSON array.
Output:
"""
)


# Try to strip response to get valid JSON
json_data = strip_to_json(response.text)

with open(f'artifacts/proposals/{dataset}.{run_id}.json', 'w') as f:
    if json_data:
        json.dump(json_data, f, indent=2)
    else:
        # If JSON extraction fails, save the original text
        f.write(response.text)
print(f"Generated checks saved to artifacts/proposals/{dataset}.{run_id}.json")
