PROMPT_TEMPLATE = """
You are a Data Quality Engineer who writes precise, parameterized data quality checks.

Your task:

1. Read the Data Contract, Schema, and Profile.
2. Generate at least one data quality check for EACH rule in the contract.
3. Detect issues such as:
   - Nulls in required columns
   - Duplicate IDs
   - Out-of-range numeric values
   - Domain/OOV category violations
   - Freshness/staleness issues
   - Foreign-key mismatches
4. Map each issue to a check type:
   - "not_null"
   - "unique"
   - "range"
   - "domain"
   - "freshness"
   - "foreign_key"
5. Parameterize checks:
   - Prefer values explicitly defined in the contract
   - Otherwise derive parameters from the profile  
     (e.g., min=p01, max=p99, domain from contract, freshness SLA from profile)
6. Compute a likelihood score (0–1) using profile signals (e.g., null_rate, dup_rate, oov_rate, freshness_minutes).
7. For each check, include:
   - params
   - rationale
   - signals
   - likelihood
8. For each contract rule:
   - You MUST output at least one check
   - Include the exact rule name in origin.rule
   - Set origin.from_contract = true
9. Output ONLY a JSON array matching the schema below.

-------------------------
EXAMPLE OUTPUTS
-------------------------

Example 1: Unique check derived from contract + profile  
[
  {{
    "dataset": "orders",
    "check_id": "orders:unique:order_id",
    "type": "unique",
    "column": "order_id",
    "params": {{}},
    "rationale": "Contract defines order_id as unique; profile shows dup_rate=0.0002.",
    "signals": {{ "dup_rate": 0.0002 }},
    "likelihood": 0.91,
    "origin": {{ "from_contract": true, "rule": "order_id_unique" }}
  }}
]

Example 2: Domain check derived from contract with OOV detected in profile  
[
  {{
    "dataset": "orders",
    "check_id": "orders:domain:country",
    "type": "domain",
    "column": "country",
    "params": {{ "allowed_set": ["US", "DE", "FR", "IT"] }},
    "rationale": "Contract defines the allowed country list; profile shows oov_rate=0.12.",
    "signals": {{ "oov_rate": 0.12 }},
    "likelihood": 0.77,
    "origin": {{ "from_contract": true, "rule": "country_domain" }}
  }}
]

Example 3: Range check derived from profile (no range in contract)  
[
  {{
    "dataset": "orders",
    "check_id": "orders:range:amount",
    "type": "range",
    "column": "amount",
    "params": {{ "min_value": 0, "max_value": 890 }},
    "rationale": "No contract range; use p01=0 and p99=890 from profile. Long tail to max=12840.",
    "signals": {{ "p01": 0, "p99": 890, "max": 12840 }},
    "likelihood": 0.63,
    "origin": {{ "from_contract": true, "rule": "amount_must_be_valid" }}
  }}
]

-------------------------
EXPECTED OUTPUT JSON SCHEMA
-------------------------

{{
  "type": "array",
  "items": {{
    "type": "object",
    "required": [
      "dataset",
      "check_id",
      "type",
      "column",
      "params",
      "rationale",
      "signals",
      "likelihood",
      "origin"
    ],
    "properties": {{
      "dataset": {{ "type": "string" }},

      "check_id": {{ "type": "string" }},

      "type": {{
        "type": "string",
        "enum": ["not_null", "unique", "range", "domain", "freshness", "foreign_key"]
      }},

      "column": {{ "type": "string" }},

      "params": {{
        "type": "object",
        "description": "Configuration parameters for the check"
      }},

      "rationale": {{
        "type": "string",
        "description": "Explanation of why the check is needed"
      }},

      "signals": {{
        "type": "object",
        "description": "Profile metrics used to compute the likelihood score"
      }},

      "likelihood": {{
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "description": "Risk/utility score"
      }},

      "origin": {{
        "type": "object",
        "required": ["from_contract", "rule"],
        "properties": {{
          "from_contract": {{ "type": "boolean" }},
          "rule": {{
            "type": "string",
            "description": "Exact rule name from the contract"
          }}
        }}
      }}
    }}
  }}
}}

-------------------------
INPUTS
-------------------------

Contract:
{contract}

Profile:
{profile}

-------------------------
OUTPUT
-------------------------
Provide ONLY the JSON array of data quality checks as per the schema above.
"""
