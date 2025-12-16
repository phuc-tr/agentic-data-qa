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
        # print(f"Added expectation: {expectation.expectation_type}") # Uncomment for debugging
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

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToMatchRegex,
    meta={"check_id": "raddb:domain:nasportid_format"},
    column="nasportid",
    regex="^Uniq-Sess-ID\\d{2}$"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "raddb:domain:nasporttype_valid_values"},
    column="nasporttype",
    value_set=[
        "Virtual",
        "ISDN"
    ]
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB,
    meta={"check_id": "raddb:custom:acctstoptime_later_than_acctstarttime"},
    column_A="acctstoptime",
    column_B="acctstarttime",
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnQuantileValuesToBeBetween,
    meta={"check_id": "raddb:range:acctsessiontime_95th_percentile"},
    column="acctsessiontime",
    quantile_ranges={
        "quantiles": [0.0, 0.95, 1.0],
        "value_ranges": [[None, None], [None, 30000], [None, None]]
    }
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:calledstationid"},
    column="calledstationid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:callingstationid"},
    column="callingstationid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeInSet,
    meta={"check_id": "raddb:domain:acctterminatecause_valid_values"},
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
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"check_id": "raddb:not_null:created_at"},
    column="created_at"
)

current_datetime = datetime.datetime.now(datetime.timezone.utc)
freshness_threshold_hours = 25
min_created_at = current_datetime - datetime.timedelta(hours=freshness_threshold_hours)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnMaxToBeBetween,
    meta={"check_id": "raddb:freshness:created_at"},
    column="created_at",
    min_value=min_created_at.strftime("%Y-%m-%d %H:%M:%S%z"),
    parse_strings_as_datetimes=True,
    strict_min=False,
    strict_max=False
)