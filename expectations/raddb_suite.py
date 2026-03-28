import great_expectations as gx
import datetime

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

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeUnique,
    meta={"check_id": "radacct:unique:radacctid"},
    column="radacctid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "radacct:not_null:radacctid"},
    column="radacctid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "radacct:not_null:acctsessionid"},
    column="acctsessionid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeUnique,
    meta={"check_id": "radacct:unique:acctuniqueid"},
    column="acctuniqueid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "radacct:domain:acctterminatecause"},
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

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "radacct:range:acctinterval"},
    column="acctinterval",
    min_value=0,
    max_value=86580
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "radacct:range:acctsessiontime"},
    column="acctsessiontime",
    min_value=0,
    max_value=291240
)