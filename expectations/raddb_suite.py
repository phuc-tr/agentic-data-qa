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
        print(f"Added expectation: {expectation.expectation_type} for column '{kwargs.get('column')}'")
    except Exception as e:
        print(f"Error creating expectation {expectation_fn.__name__}: {e}")

decisions_json = {
  "radacct:unique:radacctid": {
    "likelihood": 1.0,
    "evidence": 0.0,
    "confidence": 0.5,
    "go": true
  },
  "radacct:not_null:radacctid": {
    "likelihood": 1.0,
    "evidence": 0.0,
    "confidence": 0.5,
    "go": true
  },
  "radacct:not_null:acctsessionid": {
    "likelihood": 1.0,
    "evidence": 0.0,
    "confidence": 0.5,
    "go": true
  },
  "radacct:unique:acctuniqueid": {
    "likelihood": 1.0,
    "evidence": 0.0,
    "confidence": 0.5,
    "go": true
  },
  "radacct:range:acctstoptime_acctstarttime_logicalConsistency": {
    "likelihood": 0.9,
    "evidence": 0.0,
    "confidence": 0.4600000000000001,
    "go": true
  },
  "radacct:in_set:acctterminatecause_domainValueCheck": {
    "likelihood": 0.85,
    "evidence": 0.0,
    "confidence": 0.44000000000000006,
    "go": true
  },
  "radacct:freshness:created_at_freshnessCheck": {
    "likelihood": 0.1,
    "evidence": 0.01,
    "confidence": 0.14400000000000002,
    "go": false
  }
}

# Load the decisions JSON
decisions = decisions_json

# Filter the expectations based on the 'go' flag
if decisions.get("radacct:unique:radacctid", {}).get("go"):
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToBeUnique,
        meta={"check_id": "radacct:unique:radacctid"},
        column="radacctid"
    )

if decisions.get("radacct:not_null:radacctid", {}).get("go"):
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToNotBeNull,
        meta={"check_id": "radacct:not_null:radacctid"},
        column="radacctid"
    )

if decisions.get("radacct:not_null:acctsessionid", {}).get("go"):
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToNotBeNull,
        meta={"check_id": "radacct:not_null:acctsessionid"},
        column="acctsessionid"
    )

if decisions.get("radacct:unique:acctuniqueid", {}).get("go"):
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToBeUnique,
        meta={"check_id": "radacct:unique:acctuniqueid"},
        column="acctuniqueid"
    )

if decisions.get("radacct:range:acctstoptime_acctstarttime_logicalConsistency", {}).get("go"):
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB,
        meta={"check_id": "radacct:range:acctstoptime_acctstarttime_logicalConsistency"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=True
    )

if decisions.get("radacct:in_set:acctterminatecause_domainValueCheck", {}).get("go"):
    safe_add_expectation(
        suite,
        gx.expectations.ExpectColumnValuesToBeInSet,
        meta={"check_id": "radacct:in_set:acctterminatecause_domainValueCheck"},
        column="acctterminatecause",
        value_set=[
            "User-Request",
            "Admin-Reset",
            "Host-Request",
            "NAS-Error",
            "Port-Error",
            "Service-Unvaliable"
        ]
    )

# The 'freshness' check is marked as 'go': false in the decisions JSON, so it's not included.
# if decisions.get("radacct:freshness:created_at_freshnessCheck", {}).get("go"):
#     now_utc = datetime.datetime.now(datetime.timezone.utc)
#     max_allowed_time = now_utc - datetime.timedelta(minutes=60)
#     safe_add_expectation(
#         suite,
#         gx.expectations.ExpectColumnMaxToBeBetween,
#         meta={"check_id": "radacct:freshness:created_at_freshnessCheck"},
#         column="created_at",
#         min_value=max_allowed_time.isoformat(),
#         parse_strings_as_datetimes=True
#     )