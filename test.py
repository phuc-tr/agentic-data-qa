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

# Primary key: radacctid
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

# Required: acctsessionid
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:acctsessionid"},
    column="acctsessionid"
)

# Unique: acctuniqueid
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:acctuniqueid"},
    column="acctuniqueid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeUnique,
    meta={"check_id": "raddb:unique:acctuniqueid"},
    column="acctuniqueid"
)

# nasportid: not null (derived from quality text "Uniq-Sess-IDXX" – we enforce non-null; pattern could be added later)
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:nasportid"},
    column="nasportid"
)

# Domain constraints
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
    value_set=[
        "User-Request",
        "Admin-Reset",
        "Host-Request",
        "NAS-Error",
        "Port-Error",
        "Service-Unvaliable",
    ]
)

# acctstoptime must be later than acctstarttime
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB,
    meta={"check_id": "raddb:acctstoptime:greater_than_acctstarttime"},
    column_A="acctstoptime",
    column_B="acctstarttime"
)

# Session time range (95% < 30000 seconds) – implemented as a hard upper bound for now
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "raddb:range:acctsessiontime"},
    column="acctsessiontime",
    min_value=0,
    max_value=30000
)

# calledstationid nulls < 10%
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:nulls_lt_10pct:calledstationid"},
    column="calledstationid",
    mostly=0.9  # at least 90% non-null
)

# callingstationid nulls < 10%
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:nulls_lt_10pct:callingstationid"},
    column="callingstationid",
    mostly=0.9
)

# Freshness: created_at within last 25 hours
safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"check_id": "raddb:freshness:created_at"},
    column="created_at",
    min_value=(datetime.now() - timedelta(hours=25)),
    max_value=datetime.now()
)