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

# radacctid not null
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:radacctid"},
    column="radacctid"
)

# radacctid unique
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnUniqueValueCountToBeEqual,
    meta={"check_id": "raddb:unique:radacctid"},
    column="radacctid",
    unique_count=1
)

# acctsessionid not null
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:acctsessionid"},
    column="acctsessionid"
)

# acctuniqueid unique
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnUniqueValueCountToBeEqual,
    meta={"check_id": "raddb:unique:acctuniqueid"},
    column="acctuniqueid",
    unique_count=1
)

# nasportid format
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValueRegexMatch,
    meta={"check_id": "raddb:format:nasportid"},
    column="nasportid",
    regex="^Uniq-Sess-ID[0-9]+$"
)

# nasporttype domain
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "raddb:domain:nasporttype"},
    column="nasporttype",
    value_set=["Virtual", "ISDN"]
)

# acctterminatecause domain
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "raddb:domain:acctterminatecause"},
    column="acctterminatecause",
    value_set=["User-Request", "Admin-Reset", "Host-Request", "NAS-Error", "Port-Error", "Service-Unvaliable"]
)

# acctstoptime after acctstarttime
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnPairValuesToBeInSet,
    meta={"check_id": "raddb:relationship:acctstoptime_acctstarttime"},
    column_A="acctstoptime",
    column_B="acctstarttime",
    value_set=[(x, y) for x in range(100) for y in range(x)]
)

# acctsessiontime range
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "raddb:range:acctsessiontime"},
    column="acctsessiontime",
    min_value=0,
    max_value=30000
)

# acctsessiontime 95th percentile
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnQuantileValuesToBeBetween,
    meta={"check_id": "raddb:quantile:acctsessiontime"},
    column="acctsessiontime",
    quantile_ranges={
        "0.95": {"min_value": 0, "max_value": 30000}
    }
)

# calledstationid not null
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:calledstationid"},
    column="calledstationid"
)

# calledstationid null rate
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionOfUniqueValuesToBeBetween,
    meta={"check_id": "raddb:null_rate:calledstationid"},
    column="calledstationid",
    min_proportion=0.9,
    max_proportion=1.0,
    null_values=[None]
)

# callingstationid not null
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:callingstationid"},
    column="callingstationid"
)

# callingstationid null rate
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnProportionOfUniqueValuesToBeBetween,
    meta={"check_id": "raddb:null_rate:callingstationid"},
    column="callingstationid",
    min_proportion=0.9,
    max_proportion=1.0,
    null_values=[None]
)

# created_at freshness
threshold_date = datetime.now() - timedelta(days=25)
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeGreaterThan,
    meta={"check_id": "raddb:freshness:created_at"},
    column="created_at",
    min_value=threshold_date
)