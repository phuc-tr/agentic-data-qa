import great_expectations as gx

context = gx.get_context()

suite_name = "raddb_expectation_suite"
suite = gx.ExpectationSuite(suite_name)
context.save_expectation_suite(suite)

def safe_add_expectation(suite, expectation_fn, **kwargs):
    try:
        expectation = expectation_fn(**kwargs)
        suite.add_expectation(expectation)
        print(f"Added expectation: {expectation.expectation_type}")
    except Exception as e:
        print(f"Error creating expectation {expectation_fn.__name__}: {e}")

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"table": "raddb", "expectation_type": "not_null", "column": "radacctid"},
    column="radacctid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnUniqueValueCountToBeBetween,
    meta={"table": "raddb", "expectation_type": "unique", "column": "radacctid"},
    column="radacctid",
    min_value=1,
    max_value=1
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"table": "raddb", "expectation_type": "not_null", "column": "acctsessionid"},
    column="acctsessionid"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnUniqueValueCountToBeBetween,
    meta={"table": "raddb", "expectation_type": "unique", "column": "acctuniqueid"},
    column="acctuniqueid",
    min_value=1,
    max_value=1
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnDistinctValuesToBeInSet,
    meta={"table": "raddb", "expectation_type": "domain", "column": "nasporttype"},
    column="nasporttype",
    value_set=["Virtual", "ISDN"]
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={"table": "raddb", "expectation_type": "range", "column": "acctsessiontime"},
    column="acctsessiontime",
    min_value=0,
    max_value=30000
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={"table": "raddb", "expectation_type": "not_null", "column": "created_at"},
    column="created_at"
)