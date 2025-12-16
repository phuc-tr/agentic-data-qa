import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid: required, unique, primary key
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:radacctid"},
        column="radacctid"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "raddb:unique:radacctid"},
        column="radacctid"
    )
)

# acctsessionid: required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctsessionid"},
        column="acctsessionid"
    )
)

# acctuniqueid: required, unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctuniqueid"},
        column="acctuniqueid"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        meta={"check_id": "raddb:unique:acctuniqueid"},
        column="acctuniqueid"
    )
)

# nasportid text rule: "Uniq-Sess-IDXX" (simple pattern: starts with 'Uniq-Sess-ID')
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "raddb:format:nasportid"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID.*$",
        mostly=1.0
    )
)

# nasporttype: domain constraint
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "raddb:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
        mostly=0.999  # mustBeLessThan:1 invalid values ⇒ allow at most 0.1% failures
    )
)

# acctstoptime later than acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "raddb:range:acctstoptime_after_start"},
        column_A="acctstoptime",
        column_B="acctstarttime"
    )
)

# acctsessiontime: 95% of values < 30000
suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "raddb:range:acctsessiontime_p95"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]]
        }
    )
)

# calledstationid: null values < 10%  ⇒ non-null proportion between 0.9 and 1
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "raddb:not_null:calledstationid"},
        column="calledstationid",
        min_value=0.9,
        max_value=1.0
    )
)

# callingstationid: null values < 10%  ⇒ non-null proportion between 0.9 and 1
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "raddb:not_null:callingstationid"},
        column="callingstationid",
        min_value=0.9,
        max_value=1.0
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
            "Service-Unvaliable"
        ],
        mostly=0.999
    )
)

# created_at: required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:created_at"},
        column="created_at"
    )
)

# Freshness: youngest created_at within last 25 hours
suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "raddb:freshness:created_at"},
        column="created_at",
        min_value=(datetime.datetime.utcnow() - datetime.timedelta(hours=25)).isoformat(),
        max_value=datetime.datetime.utcnow().isoformat()
    )
)