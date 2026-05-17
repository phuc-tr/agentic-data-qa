import json
import subprocess
import uuid
import yaml
from pathlib import Path
import great_expectations as gx


def _get_schema_names(contract_path: str) -> list[str]:
    """Return all schema/model names from the contract YAML."""
    with open(contract_path) as f:
        doc = yaml.safe_load(f)
    # ODCS v3: schema is a list of objects with a 'name' key
    if isinstance(doc.get("schema"), list):
        return [s["name"] for s in doc["schema"] if isinstance(s, dict) and "name" in s]
    # Older spec: models is a dict keyed by name
    if isinstance(doc.get("models"), dict):
        return list(doc["models"].keys())
    return []


def _export_one(contract_path: str, schema_name: str | None = None) -> dict:
    cmd = ["datacontract", "export", "--format", "great-expectations", "--engine", "pandas", contract_path]
    if schema_name:
        cmd += ["--schema-name", schema_name]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        label = f"--schema-name {schema_name}" if schema_name else "no schema"
        raise RuntimeError(f"datacontract export ({label}) failed:\n{result.stderr}")
    return json.loads(result.stdout)


def build_base_suite_from_cli(
    contract_path: str, suite_name: str = "expectation_suite"
) -> int:
    """
    Run datacontract CLI export and write the JSON directly to the GX expectations
    store. Automatically iterates all schemas in the contract and merges their
    expectations into a single suite.
    """
    schemas = _get_schema_names(contract_path)

    if len(schemas) <= 1:
        cli_data = _export_one(contract_path, schema_name=schemas[0] if schemas else None)
    else:
        all_expectations: list[dict] = []
        for schema in schemas:
            data = _export_one(contract_path, schema_name=schema)
            all_expectations.extend(data.get("expectations", []))
        cli_data = {"expectations": all_expectations}

    # Initialise GX file context so the gx/ directory structure is created.
    gx.get_context(mode="file")

    # Patch name and add UUIDs expected by the GX file store.
    cli_data["name"] = suite_name
    cli_data["id"] = str(uuid.uuid4())
    for exp in cli_data.get("expectations", []):
        exp.setdefault("id", str(uuid.uuid4()))

    Path("gx/expectations").mkdir(parents=True, exist_ok=True)
    with open(f"gx/expectations/{suite_name}.json", "w") as f:
        json.dump(cli_data, f, indent=2)

    return len(cli_data.get("expectations", []))


def extract_unresolved_rules(contract: dict) -> list[dict]:
    """
    Return all quality rules that the datacontract CLI does not handle.

    The CLI covers only: column types, uniqueness, and column-list order.
    Everything else is unresolved and must be handled by the LLM:
      - required / primaryKey  → not_null expectations
      - quality[*]             → metric (invalidValues, nullValues), sql, text rules
      - servicelevels.freshness → freshness expectations
    """
    unresolved: list[dict] = []

    for model_name, model_def in contract.get("models", {}).items():
        if not isinstance(model_def, dict):
            continue

        fields = model_def.get("fields", {})
        for field_name, field_def in fields.items():
            if not isinstance(field_def, dict):
                continue

            # required / primaryKey → not_null (CLI skips these)
            if field_def.get("required") or field_def.get("primaryKey"):
                unresolved.append({
                    "model": model_name,
                    "field": field_name,
                    "field_type": field_def.get("type", "string"),
                    "description": field_def.get("description", ""),
                    "rule": {"type": "required"},
                })

            # ALL quality blocks (CLI ignores the entire quality key)
            for q in field_def.get("quality", []):
                if not isinstance(q, dict):
                    continue
                unresolved.append({
                    "model": model_name,
                    "field": field_name,
                    "field_type": field_def.get("type", "string"),
                    "description": field_def.get("description", ""),
                    "rule": q,
                })

        # Model-level quality rules
        for q in model_def.get("quality", []):
            if not isinstance(q, dict):
                continue
            unresolved.append({
                "model": model_name,
                "field": q.get("field", ""),
                "field_type": "",
                "description": "",
                "rule": q,
            })

    # Service-level freshness
    sla = contract.get("servicelevels") or contract.get("serviceLevel") or {}
    freshness = sla.get("freshness", {})
    if isinstance(freshness, dict) and freshness:
        unresolved.append({
            "model": "",
            "field": freshness.get("timestampField", ""),
            "field_type": "timestamp",
            "description": freshness.get("description", ""),
            "rule": {
                "type": "freshness",
                "threshold": freshness.get("threshold"),
                "timestampField": freshness.get("timestampField"),
            },
        })

    return unresolved


def build_llm_fragment(unresolved: list[dict]) -> str:
    """
    Build a minimal YAML fragment containing only the unresolved fields and their rules.
    This — and nothing else — is sent to the LLM.
    """
    fragment: dict = {}
    for item in unresolved:
        field = item["field"]
        if field not in fragment:
            fragment[field] = {
                "type": item["field_type"],
                "description": item["description"],
                "rules": [],
            }
        fragment[field]["rules"].append(item["rule"])

    return yaml.dump({"unresolved_fields": fragment}, default_flow_style=False, sort_keys=False)
