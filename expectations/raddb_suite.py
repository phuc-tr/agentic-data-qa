import great_expectations as gx
import datetime
import json

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

def safe_add_expectation(suite, expectation_fn, **kwargs):
    try:
        expectation = expectation_fn(**kwargs)
        suite.add_expectation(expectation)
        print(f"Added expectation: {expectation.expectation_type}")
    except Exception as e:
        print(f"Error creating expectation {expectation_fn.__name__}: {e}")

decisions_json = """
{
  "radacct:unique:acctuniqueid": {
    "likelihood": 0.95,
    "evidence": 0.0,
    "confidence": 0.48,
    "go": true
  },
  "radacct:not_null:radacctid": {
    "likelihood": 0.95,
    "evidence": 0.0,
    "confidence": 0.48,
    "go": true
  },
  "radacct:not_null:acctsessionid": {
    "likelihood": 0.95,
    "evidence": 0.0,
    "confidence": 0.48,
    "go": true
  },
  "radacct:unique:radacctid": {
    "likelihood": 0.95,
    "evidence": 0.0,
    "confidence": 0.48,
    "go": true
  },
  "radacct:range:acctstoptime_ge_acctstarttime": {
    "likelihood": 0.85,
    "evidence": 0.01,
    "confidence": 0.44400000000000006,
    "go": true
  },
  "radacct:domain:acctterminatecause": {
    "likelihood": 0.7,
    "evidence": 0.0,
    "confidence": 0.38,
    "go": false
  },
  "radacct:freshness:created_at": {
    "likelihood": 0.1,
    "evidence": 0.0,
    "confidence": 0.14,
    "go": false
  }
}
"""

decisions = json.loads(decisions_json)

go_checks = {check_id for check_id, data in decisions.items() if data.get("go")}

if "radacct:unique:acctuniqueid" in go_checks:
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToBeUnique,
        meta={"check_id": "radacct:unique:acctuniqueid"},
        column="acctuniqueid"
    )

if "radacct:not_null:radacctid" in go_checks:
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToNotBeNull,
        meta={"check_id": "radacct:not_null:radacctid"},
        column="radacctid"
    )

if "radacct:not_null:acctsessionid" in go_checks:
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToNotBeNull,
        meta={"check_id": "radacct:not_null:acctsessionid"},
        column="acctsessionid"
    )

if "radacct:unique:radacctid" in go_checks:
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToBeUnique,
        meta={"check_id": "radacct:unique:radacctid"},
        column="radacctid"
    )

if "radacct:range:acctstoptime_ge_acctstarttime" in go_checks:
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB,
        meta={"check_id": "radacct:range:acctstoptime_ge_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True,
        allow_null_values=True
    )

# The following expectations are not included because their 'go' flag is false in the decisions JSON:
# radacct:domain:acctterminatecause
# radacct:freshness:created_at