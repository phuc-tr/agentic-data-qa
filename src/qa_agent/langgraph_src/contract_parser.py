import json
import subprocess
import uuid
import yaml
from pathlib import Path
import great_expectations as gx


# Maps GX expectation type strings to canonical check_type used by the evaluator
_EXPECTATION_CHECK_TYPE: dict[str, str] = {
    "expect_column_values_to_not_be_null": "not_null",
    "expect_column_values_to_be_unique": "unique",
    "expect_column_values_to_be_between": "range",
    "expect_column_values_to_be_in_set": "domain",
    "expect_column_distinct_values_to_be_in_set": "domain",
    "expect_column_distinct_values_to_equal_set": "domain",
    "expect_column_values_to_match_regex": "format",
    "expect_column_values_to_match_strftime_format": "format",
    "expect_column_values_to_match_like_pattern": "format",
}


def parse_cli_coverage(suite_json: dict) -> set[tuple[str, str]]:
    """
    Parse a GX suite JSON (as produced by the CLI in Stage 1) and return the set of
    (field, check_type) pairs it already covers, using only expectation type + kwargs.
    Expectations that already have a check_id in meta are skipped (LLM-generated).
    """
    covered: set[tuple[str, str]] = set()
    for exp in suite_json.get("expectations", []):
        if exp.get("meta", {}).get("check_id"):
            continue  # already tagged by LLM — don't count as CLI coverage
        exp_type = exp.get("type", "")
        check_type = _EXPECTATION_CHECK_TYPE.get(exp_type)
        if not check_type:
            continue
        column = exp.get("kwargs", {}).get("column")
        if column:
            covered.add((column, check_type))
    return covered


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


def extract_unresolved_rules(
    contract: dict,
    cli_coverage: set[tuple[str, str]] | None = None,
) -> list[dict]:
    """
    Return rules that the CLI did not cover and must be handled by the LLM.

    Structural rules (not_null, unique, range, domain, format) are checked against
    cli_coverage: only those absent from the CLI suite are included.
    Quality blocks (text, sql, library/metric) and freshness are always included
    because the CLI never handles them.

    If cli_coverage is None (e.g. CLI was skipped), all structural rules are included.
    """
    unresolved: list[dict] = []

    def _missing(field: str, check_type: str) -> bool:
        """True when the CLI suite does not already cover this (field, check_type)."""
        return cli_coverage is None or (field, check_type) not in cli_coverage

    for model_name, model_def in contract.get("models", {}).items():
        if not isinstance(model_def, dict):
            continue

        fields = model_def.get("fields", {})
        for field_name, field_def in fields.items():
            if not isinstance(field_def, dict):
                continue

            field_type = field_def.get("type", "string")
            desc = field_def.get("description", "")

            if (field_def.get("required") or field_def.get("primaryKey")) and _missing(field_name, "not_null"):
                unresolved.append({
                    "model": model_name, "field": field_name,
                    "field_type": field_type, "description": desc,
                    "rule": {"type": "required"},
                })

            if (field_def.get("unique") or field_def.get("primaryKey")) and _missing(field_name, "unique"):
                unresolved.append({
                    "model": model_name, "field": field_name,
                    "field_type": field_type, "description": desc,
                    "rule": {"type": "unique"},
                })

            if ("minimum" in field_def or "maximum" in field_def) and _missing(field_name, "range"):
                unresolved.append({
                    "model": model_name, "field": field_name,
                    "field_type": field_type, "description": desc,
                    "rule": {
                        "type": "range",
                        "minimum": field_def.get("minimum"),
                        "maximum": field_def.get("maximum"),
                    },
                })

            # Quality blocks — CLI never handles these
            for q in field_def.get("quality", []):
                if not isinstance(q, dict):
                    continue
                unresolved.append({
                    "model": model_name, "field": field_name,
                    "field_type": field_type, "description": desc,
                    "rule": q,
                })

        # Model-level quality rules — CLI never handles these
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

    # Service-level freshness — CLI never handles this
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
    Build a minimal YAML fragment of unresolved fields and their rules for the LLM.
    Keyed by "model.field" so same-named fields in different models are kept separate.
    """
    fragment: dict = {}
    for item in unresolved:
        model = item.get("model", "")
        field = item["field"]
        key = f"{model}.{field}" if model else field
        if key not in fragment:
            fragment[key] = {
                "model": model,
                "field": field,
                "type": item["field_type"],
                "description": item["description"],
                "rules": [],
            }
        fragment[key]["rules"].append(item["rule"])

    return yaml.dump({"unresolved_fields": fragment}, default_flow_style=False, sort_keys=False)
