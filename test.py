import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid: required, unique, primary key
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:radacctid"},
        column="radacctid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacct:unique:radacctid"},
        column="radacctid",
    )
)

# acctsessionid: required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:acctsessionid"},
        column="acctsessionid",
    )
)

# acctuniqueid: required & unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:acctuniqueid"},
        column="acctuniqueid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "radacct:unique:acctuniqueid"},
        column="acctuniqueid",
    )
)

# nasportid format: "Uniq-Sess-IDXX"
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "radacct:domain:nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9]{2}$",
    )
)

# nasporttype domain constraint
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# acctstoptime must be later than acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "radacct:range:acctstoptime_after_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
    )
)

# acctsessiontime: 95% should be < 30000 seconds
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "radacct:range:acctsessiontime_p95"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]],
        },
    )
)

# calledstationid: nulls < 10% -> non-null proportion between 0.9 and 1
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "radacct:not_null:calledstationid"},
        column="calledstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

# callingstationid: nulls < 10% -> non-null proportion between 0.9 and 1
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "radacct:not_null:callingstationid"},
        column="callingstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

# acctterminatecause domain constraint
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct:domain:acctterminatecause"},
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

# Freshness SLA: youngest row (created_at) must be within last 25 hours
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "radacct:freshness:created_at"},
        column="created_at",
        min_value=(datetime.now() - timedelta(hours=25)),
        max_value=datetime.now(),
    )
)