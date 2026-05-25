import json
import re
import yaml

CANONICAL_TYPES = {"not_null", "unique", "domain", "range", "format", "freshness", "foreign_key"}

_DESC_TYPE_MAP = [
    (["null", "missing"], "not_null"),
    (["percentile", "quantile", "range", "min", "max"], "range"),
    (["unique", "dup"], "unique"),
    (["domain", "valid", "invalid", "allowed"], "domain"),
    (["format", "regex", "pattern"], "format"),
    (["fresh", "stale", "latency"], "freshness"),
    (["foreign", "reference", "ref"], "foreign_key"),
]


def _infer_type_from_desc(desc: str) -> str:
    desc = desc.lower()
    for keywords, check_type in _DESC_TYPE_MAP:
        if any(k in desc for k in keywords):
            return check_type
    return "custom"


def extract_expected_checks(contract: dict) -> set[tuple[str, str]]:
    """
    Deterministically derive (field, check_type) pairs from a data contract YAML dict.
    Skips text-based and expression-based quality rules (non-deterministic).
    """
    checks: set[tuple[str, str]] = set()
    models = contract.get("models", {})

    for _model_name, model_def in models.items():
        if not isinstance(model_def, dict):
            continue

        fields = model_def.get("fields", {})
        for field_name, field_def in fields.items():
            if not isinstance(field_def, dict):
                continue

            is_pk = field_def.get("primaryKey", False)

            if field_def.get("required") or is_pk:
                checks.add((field_name, "not_null"))
            if field_def.get("unique") or is_pk:
                checks.add((field_name, "unique"))
            if field_def.get("enum") is not None:
                checks.add((field_name, "domain"))
            if field_def.get("pattern") is not None:
                checks.add((field_name, "format"))
            if "minimum" in field_def or "maximum" in field_def:
                checks.add((field_name, "range"))

            for q in field_def.get("quality", []):
                if not isinstance(q, dict):
                    continue
                metric = q.get("metric", "")
                qtype = q.get("type", "")
                if metric == "invalidValues":
                    checks.add((field_name, "domain"))
                elif metric == "nullValues":
                    checks.add((field_name, "not_null"))
                elif qtype == "sql" and "mustBeLessThan" in q:
                    checks.add((field_name, "range"))
                # type: text is skipped — natural language, not deterministic

        for q in model_def.get("quality", []):
            if not isinstance(q, dict):
                continue
            rule = q.get("rule", "")
            field = q.get("field", "")
            if not field:
                continue
            if rule == "accepted_values":
                checks.add((field, "domain"))
            elif rule == "regex":
                checks.add((field, "format"))
            elif rule == "unique":
                checks.add((field, "unique"))
            elif rule == "referential_integrity":
                checks.add((field, "foreign_key"))
            # custom rules are skipped — expression-based, not mappable

    # Service-level freshness
    sla = contract.get("servicelevels") or contract.get("serviceLevel") or {}
    freshness = sla.get("freshness", {})
    if isinstance(freshness, dict):
        ts_field = freshness.get("timestampField", "")
        if ts_field:
            field = ts_field.split(".")[-1]  # "radacct.acctstarttime" → "acctstarttime"
            checks.add((field, "freshness"))
        elif freshness:
            # freshness block exists but no timestampField — record a generic marker
            checks.add(("__freshness__", "freshness"))

    return checks


def extract_generated_checks(gx_content: str) -> set[tuple[str, str]]:
    """
    Parse check_ids from a GX expectation suite JSON or generated Python code.
    Normalises to (field, check_type) tuples.
    """
    checks: set[tuple[str, str]] = set()

    # Try JSON first (suite committed after execution)
    try:
        suite = json.loads(gx_content)
        for exp in suite.get("expectations", []):
            check_id = exp.get("meta", {}).get("check_id", "")
            if not check_id:
                continue
            parts = check_id.split(":")
            if len(parts) < 2:
                continue
            if len(parts) >= 3 and parts[1] in CANONICAL_TYPES:
                checks.add((parts[2], parts[1]))
            elif len(parts) >= 3 and parts[2] in CANONICAL_TYPES:
                checks.add((parts[1], parts[2]))
            elif len(parts) >= 3:
                checks.add((parts[1], _infer_type_from_desc(":".join(parts[2:]))))
            else:
                checks.add((parts[1], "unknown"))
        return checks
    except (json.JSONDecodeError, AttributeError):
        pass

    # Fallback: regex over Python code
    pattern = r'"check_id"\s*:\s*"([^"]+)"'
    for check_id in re.findall(pattern, gx_content):
        parts = check_id.split(":")
        if len(parts) < 2:
            continue
        if len(parts) >= 3 and parts[1] in CANONICAL_TYPES:
            checks.add((parts[2], parts[1]))
        elif len(parts) >= 3 and parts[2] in CANONICAL_TYPES:
            checks.add((parts[1], parts[2]))
        elif len(parts) >= 3:
            checks.add((parts[1], _infer_type_from_desc(":".join(parts[2:]))))
        else:
            checks.add((parts[1], "unknown"))

    return checks


def compute_metrics(
    expected: set[tuple[str, str]],
    generated: set[tuple[str, str]],
) -> dict:
    tp = expected & generated
    fp = generated - expected
    fn = expected - generated

    precision = len(tp) / (len(tp) + len(fp)) if generated else 0.0
    recall = len(tp) / (len(tp) + len(fn)) if expected else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tp": sorted(tp),
        "fp": sorted(fp),
        "fn": sorted(fn),
    }


def evaluate_run(contract_path: str, gx_suite_path: str, execution_passed: bool) -> dict:
    with open(contract_path) as f:
        contract = yaml.safe_load(f)
    with open(gx_suite_path) as f:
        gx_content = f.read()

    expected = extract_expected_checks(contract)
    generated = extract_generated_checks(gx_content)
    metrics = compute_metrics(expected, generated)
    metrics["execution_passed"] = execution_passed
    metrics["expected_count"] = len(expected)
    metrics["generated_count"] = len(generated)
    return metrics
