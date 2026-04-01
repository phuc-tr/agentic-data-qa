import great_expectations as gx
from great_expectations.core import ExpectationConfiguration
from datetime import datetime, timedelta

context = gx.get_context()

suite_name = "radacct_expectation_suite"
suite = context.create_expectation_suite(suite_name, overwrite_existing=True)

def safe_add_expectation(expectation_suite, expectation_type, kwargs=None, meta=None):
    kwargs = kwargs or {}
    meta = meta or {}
    try:
        expectation_config = ExpectationConfiguration(
            expectation_type=expectation_type,
            kwargs=kwargs,
            meta=meta,
        )
        expectation_suite.add_expectation(expectation_config)
        print(f"Added expectation: {expectation_type} for {kwargs.get('column', kwargs.get('column_A', 'N/A'))}")
    except Exception as e:
        print(f"Error creating expectation {expectation_type}: {e}")

# Required / primary keys
safe_add_expectation(
    suite,
    "expect_column_values_to_not_be_null",
    kwargs={"column": "radacctid"},
    meta={"check_id": "raddb:not_null:radacctid"},
)

safe_add_expectation(
    suite,
    "expect_column_values_to_be_unique",
    kwargs={"column": "radacctid"},
    meta={"check_id": "raddb:unique:radacctid"},
)

safe_add_expectation(
    suite,
    "expect_column_values_to_not_be_null",
    kwargs={"column": "acctsessionid"},
    meta={"check_id": "raddb:not_null:acctsessionid"},
)

safe_add_expectation(
    suite,
    "expect_column_values_to_not_be_null",
    kwargs={"column": "acctuniqueid"},
    meta={"check_id": "raddb:not_null:acctuniqueid"},
)

safe_add_expectation(
    suite,
    "expect_column_values_to_be_unique",
    kwargs={"column": "acctuniqueid"},
    meta={"check_id": "raddb:unique:acctuniqueid"},
)

# Domain / enumerations
safe_add_expectation(
    suite,
    "expect_column_values_to_be_in_set",
    kwargs={"column": "nasporttype", "value_set": ["Virtual", "ISDN"], "mostly": 1.0},
    meta={"check_id": "raddb:domain:nasporttype"},
)

safe_add_expectation(
    suite,
    "expect_column_values_to_be_in_set",
    kwargs={
        "column": "acctterminatecause",
        "value_set": [
            "User-Request",
            "Admin-Reset",
            "Host-Request",
            "NAS-Error",
            "Port-Error",
            "Service-Unvaliable",
        ],
        "mostly": 1.0,
    },
    meta={"check_id": "raddb:domain:acctterminatecause"},
)

# Format / regex checks
safe_add_expectation(
    suite,
    "expect_column_values_to_match_regex",
    kwargs={"column": "nasportid", "regex": r"^Uniq-Sess-ID\d{2}$"},
    meta={"check_id": "raddb:domain:nasportid_format"},
)

# Null-proportion checks (use mostly to require >=90% non-null)
safe_add_expectation(
    suite,
    "expect_column_values_to_not_be_null",
    kwargs={"column": "calledstationid", "mostly": 0.90},
    meta={"check_id": "raddb:not_null:calledstationid"},
)

safe_add_expectation(
    suite,
    "expect_column_values_to_not_be_null",
    kwargs={"column": "callingstationid", "mostly": 0.90},
    meta={"check_id": "raddb:not_null:callingstationid"},
)

# Ranges and distributions
# Basic allowable range for acctsessiontime
safe_add_expectation(
    suite,
    "expect_column_values_to_be_between",
    kwargs={"column": "acctsessiontime", "min_value": 0, "max_value": 291240, "mostly": 1.0},
    meta={"check_id": "raddb:range:acctsessiontime"},
)

# 95th percentile constraint: 95th percentile must be <= 30000
safe_add_expectation(
    suite,
    "expect_column_quantile_values_to_be_between",
    kwargs={"column": "acctsessiontime", "quantile": 0.95, "min_value": None, "max_value": 30000, "allow_relative_error": True},
    meta={"check_id": "raddb:range:acctsessiontime_95pct_under_30000"},
)

# Temporal relationship: acctstoptime must be after acctstarttime
safe_add_expectation(
    suite,
    "expect_column_pair_values_A_to_be_greater_than_B",
    kwargs={"column_A": "acctstoptime", "column_B": "acctstarttime"},
    meta={"check_id": "raddb:range:acctstoptime_after_acctstarttime"},
)

# Freshness: newest created_at must be within the last 25 hours
now = datetime.utcnow()
min_allowed = now - timedelta(hours=25)
safe_add_expectation(
    suite,
    "expect_column_max_to_be_between",
    kwargs={"column": "created_at", "min_value": min_allowed.isoformat(), "max_value": now.isoformat()},
    meta={"check_id": "raddb:freshness:created_at"},
)

# created_at required
safe_add_expectation(
    suite,
    "expect_column_values_to_not_be_null",
    kwargs={"column": "created_at"},
    meta={"check_id": "raddb:not_null:created_at"},
)

# Persist the suite
context.save_expectation_suite(suite)