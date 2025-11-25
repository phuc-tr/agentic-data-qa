PROMPT_TEMPLATE = """
You are a data quality engineer. You need to:

Read the data contract and the latest profile, then produce at least one well-parameterized checks (NOT NULL, UNIQUE, RANGE, IN-SET, FK, FRESHNESS) for each rule.
Each check includes: params, rationale, signals, and a likelihood (risk/utility) score.

Detailed steps:

1. Identify gaps & anomalies from contract + profile (e.g., required columns with nulls, IDs with duplicates, out-of-range values, OOV categories, staleness, FK mismatches).
2. Map issues to check types: NOT NULL, UNIQUE, RANGE, IN-SET/DOMAIN, FRESHNESS, FK.
3. Parameterize checks: prefer contract values; if absent, use profile stats (e.g., RANGE min=p01, max=p99; FRESHNESS from SLA; IN-SET from contract domain).
4. Compute a likelihood score (0–1) per proposal from profile signals (e.g., null_rate, dup_rate, oov_rate, freshness delay).
5. Output the name of the contract rules as exactly shown in the contract in the origin field.
6. Make sure each rule from the contract has at least one associated check in the output.


Example output:
{{
  "dataset": "orders",
  "proposals": [
    {{
      "check_id": "orders:unique:order_id",
      "type": "unique",
      "column": "order_id",
      "params": {{}},
      "rationale": "Contract says unique; distinct_ratio=1.0",
      "signals": {{"distinct_ratio": 1.0}},
      "likelihood": 0.80,
      "origin": {{"from_contract": true, "rule": <rule_name_from_contract>}}
    }},
    {{
      "check_id": "orders:domain:country",
      "type": "domain",
      "column": "country",
      "params": {{"allowed_set": ["US", "DE", "IT", "FR"]}},
      "rationale": "Contract domain; observed 38 OOV values",
      "signals": {{"oov_rate": 0.235}},
      "likelihood": 0.73,
      "origin": {{"from_contract": true, "rule": <rule_name_from_contract>}}
    }},
    {{
      "check_id": "orders:freshness:created_at",
      "type": "freshness",
      "column": "created_at",
      "params": {{"max_delay_min": 30}},
      "rationale": "SLA 30m; observed 69m",
      "signals": {{"freshness_minutes": 69}},
      "likelihood": 0.88,
      "origin": {{"from_contract": true, "rule": <rule_name_from_contract>}}
    }},
    {{
      "check_id": "orders:range:amount",
      "type": "range",
      "column": "amount",
      "params": {{"min_value": 0, "max_value": 890}},
      "rationale": "Use p99=890 as upper bound; long tail to 12840",
      "signals": {{"p99": 890, "max": 12840}},
      "likelihood": 0.55,
      "origin": {{"from_profile": true, "rule": <rule_name_from_contract>}}
    }}
  ]
}}

Contract:
{contract}

Schema:
{schema}

Profile:
{profile}

Output the checks as a JSON array.
Output:
"""
