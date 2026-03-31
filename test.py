import great_expectations as gx
from datetime import datetime, timedelta

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# radacctid: required, unique, reasonable range
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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:radacctid"},
        column="radacctid",
        min_value=999_997.98,
        max_value=1_000_099.01,
    )
)

# acctsessionid: required
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:acctsessionid"},
        column="acctsessionid",
    )
)

# acctuniqueid: required, unique
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

# nasportid: text format rule "Uniq-Sess-IDXX"
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "radacct:domain:nasportid"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID.*$",
    )
)

# nasporttype: constrained domain
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "radacct:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# acctstoptime > acctstarttime
suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "radacct:range:acctstoptime_gt_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=False,
    )
)

# acctinterval: non-negative reasonable range
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctinterval"},
        column="acctinterval",
        min_value=0.0,
        max_value=86_580.01,
    )
)

# acctsessiontime: business constraint 95% < 30000, plus overall range bands
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctsessiontime"},
        column="acctsessiontime",
        min_value=0,
        max_value=30_000,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctsessiontime_profile_band"},
        column="acctsessiontime",
        min_value=39.74,
        max_value=291_240.43,
    )
)

# acctinputoctets: profile-based range
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctinputoctets"},
        column="acctinputoctets",
        min_value=258.06,
        max_value=4_157_407_489.94,
    )
)

# acctoutputoctets: profile-based range
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:range:acctoutputoctets"},
        column="acctoutputoctets",
        min_value=259.3,
        max_value=41_782_664_281.47005,
    )
)

# calledstationid: at most 10% null => at least 90% non-null
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "radacct:not_null:calledstationid"},
        column="calledstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

# callingstationid: at most 10% null => at least 90% non-null
suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "radacct:not_null:callingstationid"},
        column="callingstationid",
        min_value=0.9,
        max_value=1.0,
    )
)

# acctterminatecause: constrained domain
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

# created_at: required and freshness (age of youngest row < 25h)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "radacct:not_null:created_at"},
        column="created_at",
    )
)

max_age_hours = 25
cutoff_datetime = datetime.utcnow() - timedelta(hours=max_age_hours)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "radacct:freshness:created_at"},
        column="created_at",
        min_value=cutoff_datetime.isoformat(),
        max_value=datetime.utcnow().isoformat(),
    )
)