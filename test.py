import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid: required, unique, primary key
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:radacctid"},
        column="radacctid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "raddb:unique:radacctid"},
        column="radacctid",
    )
)

# acctsessionid: required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctsessionid"},
        column="acctsessionid",
    )
)

# acctuniqueid: required, unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctuniqueid"},
        column="acctuniqueid",
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "raddb:unique:acctuniqueid"},
        column="acctuniqueid",
    )
)

# nasportid: text format "Uniq-Sess-IDXX"
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "raddb:format:nasportid"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID\d{2}$",
    )
)

# nasporttype: domain constraint
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "raddb:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# acctstoptime > acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "raddb:acctstoptime:greater_than_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
    )
)

# acctsessiontime: non‑negative and 95% < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:range:acctsessiontime"},
        column="acctsessiontime",
        min_value=0,
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "raddb:acctsessiontime:95th_percentile"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[0, 30000]],
        },
        allow_relative_error=False,
    )
)

# calledstationid: null values < 10%
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeNull(
        meta={"check_id": "raddb:calledstationid:null_proportion"},
        column="calledstationid",
        mostly=0.10,
    )
)

# callingstationid: null values < 10%
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeNull(
        meta={"check_id": "raddb:callingstationid:null_proportion"},
        column="callingstationid",
        mostly=0.10,
    )
)

# callingstationid not null for majority of rows (foreign-key-like behavior)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:foreign_key:callingstationid"},
        column="callingstationid",
        mostly=0.90,
    )
)

# acctterminatecause: domain constraint
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "raddb:domain:acctterminatecause"},
        column="acctterminatecause",
        value_set=[
            "User-Request",
            "Admin-Reset",
            "Host-Request",
            "NAS-Error",
            "Port-Error",
            "Service-Unvaliable",
        ],
    )
)

# Freshness on created_at: youngest row <= 25h old
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:freshness:created_at"},
        column="created_at",
        min_value=datetime.now() - timedelta(hours=25),
        max_value=datetime.now(),
    )
)