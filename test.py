import datetime
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

# ------------------------
# radacctid
# ------------------------
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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:radacctid"},
        column="radacctid",
        type_="INTEGER",
    )
)

# ------------------------
# acctsessionid
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctsessionid"},
        column="acctsessionid",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:acctsessionid"},
        column="acctsessionid",
        type_="VARCHAR",
    )
)

# ------------------------
# acctuniqueid
# ------------------------
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

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:acctuniqueid"},
        column="acctuniqueid",
        type_="VARCHAR",
    )
)

# ------------------------
# realm
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:realm"},
        column="realm",
        type_="VARCHAR",
    )
)

# ------------------------
# nasportid
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:nasportid"},
        column="nasportid",
        type_="VARCHAR",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        meta={"check_id": "raddb:domain:nasportid_format"},
        column="nasportid",
        regex=r"^Uniq-Sess-ID[0-9A-Za-z]{2}$",
    )
)

# ------------------------
# nasporttype
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:nasporttype"},
        column="nasporttype",
        type_="VARCHAR",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        meta={"check_id": "raddb:domain:nasporttype"},
        column="nasporttype",
        value_set=["Virtual", "ISDN"],
    )
)

# ------------------------
# acctstarttime / acctupdatetime / acctstoptime
# ------------------------
for col in ["acctstarttime", "acctupdatetime", "acctstoptime"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"raddb:type:{col}"},
            column=col,
            type_="DATETIME",
        )
    )

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:acctstarttime"},
        column="acctstarttime",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        meta={"check_id": "raddb:range:acctstoptime_after_start"},
        column_A="acctstoptime",
        column_B="acctstarttime",
        or_equal=False,
    )
)

# ------------------------
# acctinterval
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:acctinterval"},
        column="acctinterval",
        type_="INTEGER",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:range:acctinterval_non_negative"},
        column="acctinterval",
        min_value=0,
        max_value=None,
    )
)

# ------------------------
# acctsessiontime
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:acctsessiontime"},
        column="acctsessiontime",
        type_="INTEGER",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:range:acctsessiontime_non_negative"},
        column="acctsessiontime",
        min_value=0,
        max_value=None,
    )
)

# ------------------------
# acctauthentic
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:acctauthentic"},
        column="acctauthentic",
        type_="VARCHAR",
    )
)

# ------------------------
# connectinfo_start / connectinfo_stop
# ------------------------
for col in ["connectinfo_start", "connectinfo_stop"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"raddb:type:{col}"},
            column=col,
            type_="VARCHAR",
        )
    )

# ------------------------
# acctinputoctets / acctoutputoctets
# ------------------------
for col in ["acctinputoctets", "acctoutputoctets"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"raddb:type:{col}"},
            column=col,
            type_="INTEGER",
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            meta={"check_id": f"raddb:range:{col}_non_negative"},
            column=col,
            min_value=0,
            max_value=None,
        )
    )

# ------------------------
# calledstationid / callingstationid
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:calledstationid"},
        column="calledstationid",
        type_="VARCHAR",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "raddb:not_null:calledstationid"},
        column="calledstationid",
        min_value=0.9,  # <= 10% nulls
        max_value=1.0,
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:callingstationid"},
        column="callingstationid",
        type_="VARCHAR",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
        meta={"check_id": "raddb:not_null:callingstationid"},
        column="callingstationid",
        min_value=0.9,  # <= 10% nulls
        max_value=1.0,
    )
)

# ------------------------
# acctterminatecause
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:acctterminatecause"},
        column="acctterminatecause",
        type_="VARCHAR",
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
        ],
    )
)

# ------------------------
# servicetype / framedprotocol
# ------------------------
for col in ["servicetype", "framedprotocol"]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"raddb:type:{col}"},
            column=col,
            type_="VARCHAR",
        )
    )

# ------------------------
# IPv6 related fields
# ------------------------
for col in [
    "framedipv6address",
    "framedipv6prefix",
    "framedinterfaceid",
    "delegatedipv6prefix",
]:
    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeOfType(
            meta={"check_id": f"raddb:type:{col}"},
            column=col,
            type_="VARCHAR",
        )
    )

# ------------------------
# created_at + freshness
# ------------------------
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={"check_id": "raddb:not_null:created_at"},
        column="created_at",
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeOfType(
        meta={"check_id": "raddb:type:created_at"},
        column="created_at",
        type_="TIMESTAMP",
    )
)

# Freshness: created_at within last 25 hours of run time
now = datetime.datetime.utcnow()
freshness_cutoff = now - datetime.timedelta(hours=25)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={"check_id": "raddb:freshness:created_at"},
        column="created_at",
        min_value=freshness_cutoff.isoformat(),
        max_value=None,
    )
)