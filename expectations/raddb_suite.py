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
    meta={"check_id": "raddb:not_null:radacctid"},
    column="radacctid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeUnique,
    meta={"check_id": "raddb:unique:radacctid"},
    column="radacctid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:acctsessionid"},
    column="acctsessionid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeUnique,
    meta={"check_id": "raddb:unique:acctuniqueid"},
    column="acctuniqueid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "raddb:domain:nasporttype"},
    column="nasporttype",
    value_set=["Virtual", "ISDN"]
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "raddb:domain:acctterminatecause"},
    column="acctterminatecause",
    value_set=["User-Request", "Admin-Reset", "Host-Request", "NAS-Error", "Port-Error", "Service-Unvaliable"]
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "raddb:range:acctsessiontime"},
    column="acctsessiontime",
    min_value=0,
    max_value=291240
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "raddb:freshness:created_at"},
    column="created_at",
    min_value=(datetime.now() - timedelta(hours=25)).strftime("%Y-%m-%d %H:%M:%S"),
    max_value=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnQuantileValuesToBeBetween,
    meta={"check_id": "raddb:quantile:acctsessiontime"},
    column="acctsessiontime",
    quantile_ranges=[
        {"quantile": 0.95, "min_value": 0, "max_value": 30000}
    ]
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionOfUniqueValuesToBeBetween,
    meta={"check_id": "raddb:proportion:acctuniqueid"},
    column="acctuniqueid",
    min_value=0.9,
    max_value=1.0
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween,
    meta={"check_id": "raddb:proportion:calledstationid"},
    column="calledstationid",
    min_value=0.9,
    max_value=1.0
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween,
    meta={"check_id": "raddb:proportion:callingstationid"},
    column="callingstationid",
    min_value=0.9,
    max_value=1.0
)