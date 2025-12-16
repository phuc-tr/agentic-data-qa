import great_expectations as gx
from datetime import datetime, timedelta

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
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "radacct:not_null:radacctid"},
    column="radacctid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeUnique,
    meta={"check_id": "radacct:unique:radacctid"},
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
    meta={"check_id": "radacct:domain:nasporttype"},
    column="nasporttype",
    value_set=["Virtual", "ISDN"]
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "radacct:domain:acctterminatecause"},
    column="acctterminatecause",
    value_set=["User-Request", "Admin-Reset", "Host-Request", "NAS-Error", "Port-Error", "Service-Unvaliable"]
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "radacct:range:acctsessiontime"},
    column="acctsessiontime",
    min_value=0,
    max_value=291240
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "radacct:freshness:created_at"},
    column="created_at",
    min_value=(datetime.now() - timedelta(days=25)).strftime("%Y-%m-%d %H:%M:%S"),
    max_value=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeGreaterThan,
    meta={"check_id": "radacct:acctstoptime:greater_than_acctstarttime"},
    column="acctstoptime",
    min_value=gx.expectations.core.expect_column_values_to_be_greater_than.acctstarttime
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionToBeBetween,
    meta={"check_id": "radacct:acctsessiontime:95th_percentile"},
    column="acctsessiontime",
    min_value=0,
    max_value=30000,
    quantile_range=(0.95, 1.0)
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionToBeBetween,
    meta={"check_id": "radacct:calledstationid:null_proportion"},
    column="calledstationid",
    min_value=0,
    max_value=0.1,
    quantile_range=(0.0, 0.1)
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionToBeBetween,
    meta={"check_id": "radacct:callingstationid:null_proportion"},
    column="callingstationid",
    min_value=0,
    max_value=0.1,
    quantile_range=(0.0, 0.1)
)