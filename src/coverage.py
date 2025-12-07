import json
import os
import csv
from collections import defaultdict
from typing import Dict, List, Tuple

import yaml


def load_contract_rules(dataset: str) -> List[str]:
    """Load contract and return ordered list of rule names."""
    path = f"contracts/contract.{dataset}.yaml"
    with open(path, "r") as f:
        contract_yaml = yaml.safe_load(f)
    # maintain the order defined in the contract
    rules = [q["rule"] for q in contract_yaml.get("schema")[0].get("quality", [])]
    return rules


def load_proposals(dataset: str, run_id: str) -> Tuple[Dict[str, List[str]], Dict[str, str], set]:
    """Return mapping rule->proposal_ids, proposal_id->rule (maybe None), and set of all proposal ids."""
    path = f"artifacts/proposals/{dataset}.{run_id}.json"
    with open(path, "r") as f:
        proposals = json.load(f)

    rule_to_proposal_ids: Dict[str, List[str]] = defaultdict(list)
    proposal_id_to_rule: Dict[str, str] = {}
    proposal_ids = set()

    for p in proposals:
        origin = p.get("origin") or {}
        rule = origin.get("rule")
        pid = p.get("check_id") or p.get("id") or p.get("proposal_id") or p.get("proposalId")
        if pid is None:
            pid = json.dumps(p, ensure_ascii=False)
        proposal_ids.add(pid)
        proposal_id_to_rule[pid] = rule  # may be None for profile-derived proposals
        if rule:
            rule_to_proposal_ids[rule].append(pid)

    return rule_to_proposal_ids, proposal_id_to_rule, proposal_ids


def load_existing_results(dataset: str, run_id: str) -> List[Dict]:
    """Load existing results directly from the sandbox report JSON.

    Returns a list of dicts similar to the extractor output with keys like
    `check_id`, `success`, `expectation_type`, `column`, `result`.
    """
    path = f"artifacts/sandbox/{dataset}.{run_id}.report.json"
    try:
        with open(path, "r") as f:
            report = json.load(f)
    except FileNotFoundError:
        return []

    extracted = []
    for r in report.get("results", []):
        exp_cfg = r.get("expectation_config", {}) or {}
        meta = exp_cfg.get("meta", {}) or {}
        check_id = meta.get("check_id")
        if not check_id:
            continue
        entry = {
            "check_id": check_id,
            "success": r.get("success"),
            "expectation_type": exp_cfg.get("type"),
            "column": exp_cfg.get("kwargs", {}).get("column"),
            "result": r.get("result", {}),
        }
        extracted.append(entry)

    return extracted


def build_mappings(proposal_id_to_rule: Dict[str, str], proposal_ids: set, existing_results: List[Dict]):
    """Return (rule->existing_ids, unmapped_existing_ids, proposal_only_existing).

    Only needs proposal id mappings and the existing results list.
    """
    rule_to_existing_ids = defaultdict(list)
    unmapped_existing_ids = []
    proposal_only_existing = []

    for e in existing_results:
        cid = e.get("check_id")
        if not cid:
            continue
        if cid in proposal_ids:
            mapped_rule = proposal_id_to_rule.get(cid)
            if mapped_rule:
                rule_to_existing_ids[mapped_rule].append(cid)
            else:
                proposal_only_existing.append(cid)
        else:
            unmapped_existing_ids.append(cid)

    return rule_to_existing_ids, unmapped_existing_ids, proposal_only_existing


def compute_coverages(contract_rules: List[str], rule_to_proposal_ids: Dict[str, List[str]], rule_to_existing_ids: Dict[str, List[str]]) -> Tuple[Tuple[int, int, float], Tuple[int, int, float]]:
    """Compute (covered, total, pct) for proposals and expectations."""
    total = len(contract_rules)
    proposed_rules = set(rule_to_proposal_ids.keys())
    covered_by_proposals = len(set(contract_rules).intersection(proposed_rules))
    covered_by_expectations = len(set(contract_rules).intersection(set(k for k in rule_to_existing_ids.keys())))
    prop_pct = covered_by_proposals / total if total else 1.0
    exp_pct = covered_by_expectations / total if total else 1.0
    return (covered_by_proposals, total, prop_pct), (covered_by_expectations, total, exp_pct)


def print_table(contract_rules: List[str], rule_to_proposal_ids: Dict[str, List[str]], rule_to_existing_ids: Dict[str, List[str]]):
    """Pretty-print a three-column table: Rule | Proposals | Expectations"""
    def _cell(s, w):
        s = s or ""
        s = str(s)
        if len(s) <= w:
            return s.ljust(w)
        return s[: w - 3] + "..."

    col_w = [30, 50, 50]
    hdr = f"{'Rule'.ljust(col_w[0])} | {'Proposals'.ljust(col_w[1])} | {'Expectations'.ljust(col_w[2])}"
    sep = f"{'-' * col_w[0]}-+-{'-' * col_w[1]}-+-{'-' * col_w[2]}"
    print('\n' + hdr)
    print(sep)

    table_rows = []
    for rule in sorted(contract_rules):
        prop_ids = rule_to_proposal_ids.get(rule, [])
        exist_ids = rule_to_existing_ids.get(rule, [])
        prop_str = ", ".join(prop_ids) if prop_ids else "-"
        exist_str = ", ".join(exist_ids) if exist_ids else "-"
        print(f"{_cell(rule, col_w[0])} | {_cell(prop_str, col_w[1])} | {_cell(exist_str, col_w[2])}")
        table_rows.append({
            "rule": rule,
            "proposals": prop_ids,
            "expectations": exist_ids,
        })

    return table_rows


def export_reports(dataset: str, run_id: str, summary: Dict, table_rows: List[Dict]):
    out_dir = f"artifacts/sandbox"
    out_base = f"{out_dir}/{dataset}.{run_id}.coverage"
    os.makedirs(out_dir, exist_ok=True)
    with open(out_base + ".json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(out_base + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rule", "proposals", "expectations"])
        for row in table_rows:
            writer.writerow([
                row["rule"],
                ";".join(row["proposals"]) if row["proposals"] else "",
                ";".join(row["expectations"]) if row["expectations"] else "",
            ])
    print(f"\nWrote coverage reports: {out_base}.json, {out_base}.csv")


def main(run_id: str):
    dataset = "raddb"

    contract_rules = load_contract_rules(dataset)
    rule_to_proposal_ids, proposal_id_to_rule, proposal_ids = load_proposals(dataset, run_id)
    existing_results = load_existing_results(dataset, run_id)

    rule_to_existing_ids, unmapped_existing_ids, proposal_only_existing = build_mappings(
        proposal_id_to_rule, proposal_ids, existing_results
    )

    (cov_prop_cov, cov_prop_total, cov_prop_pct), (cov_exp_cov, cov_exp_total, cov_exp_pct) = compute_coverages(
        contract_rules, rule_to_proposal_ids, rule_to_existing_ids
    )

    print(f"✅ Proposal coverage: {cov_prop_cov}/{cov_prop_total} rules covered ({cov_prop_pct:.2%})")
    print(f"✅ Expectations coverage: {cov_exp_cov}/{cov_exp_total} rules covered ({cov_exp_pct:.2%})")

    table_rows = print_table(contract_rules, rule_to_proposal_ids, rule_to_existing_ids)

    summary = {
        "dataset": dataset,
        "run_id": run_id,
        "proposal_coverage": {"covered": cov_prop_cov, "total": cov_prop_total, "pct": cov_prop_pct},
        "expectation_coverage": {"covered": cov_exp_cov, "total": cov_exp_total, "pct": cov_exp_pct},
        "table": table_rows,
        "unmapped_existing": sorted(set(unmapped_existing_ids)),
        "proposal_only_existing": sorted(set(proposal_only_existing)),
    }

    try:
        export_reports(dataset, run_id, summary, table_rows)
    except Exception as e:
        print(f"Failed to write coverage outputs: {e}")

    if unmapped_existing_ids:
        print("\n⚠️ Unmapped existing check_ids (no matching proposal):")
        for cid in sorted(set(unmapped_existing_ids)):
            print(f"  - {cid}")

    if proposal_only_existing:
        print("\nℹ️ Existing checks that match proposals but aren't tied to any contract rule:")
        for cid in sorted(set(proposal_only_existing)):
            print(f"  - {cid}")

    return 0
