import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctsessionid"},
        column="acctsessionid"
    )
)

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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "raddb:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "raddb:range:acctstoptime_gt_acctstarttime"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=False
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnQuantileValuesToBeBetween(
        meta={"check_id": "raddb:range:acctsessiontime_p95_lt_30000"},
        column="acctsessiontime",
        quantile_ranges={
            "quantiles": [0.95],
            "value_ranges": [[None, 30000]]
        }
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "raddb:not_null:calledstationid"},
        column="calledstationid",
        min_value=0.9,
        max_value=1.0
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "raddb:not_null:callingstationid"},
        column="callingstationid",
        min_value=0.9,
        max_value=1.0
    )
)

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
        ]
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:created_at"},
        column="created_at"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnMaxToBeBetween(
        meta={"check_id": "raddb:freshness:created_at"},
        column="created_at",
        min_value=(datetime.datetime.utcnow() - datetime.timedelta(hours=25)).isoformat(),
        max_value=datetime.datetime.utcnow().isoformat()
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:range:acctinterval_profile_range"},
        column="acctinterval",
        min_value=0.0,
        max_value=86580.01
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:range:acctsessiontime_profile_range"},
        column="acctsessiontime",
        min_value=39.74,
        max_value=291240.43000000017
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:range:acctinputoctets_profile_range"},
        column="acctinputoctets",
        min_value=258.06,
        max_value=4157407489.9400005
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:range:acctoutputoctets_profile_range"},
        column="acctoutputoctets",
        min_value=259.3,
        max_value=41782664281.47005
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "raddb:domain:nasportid_format_hint"},
        column="nasportid",
        regex="^Uniq-Sess-ID[0-9A-Za-z]*$"
    )
)