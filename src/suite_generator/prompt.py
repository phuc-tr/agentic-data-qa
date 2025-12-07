PROMPT_TEMPLATE = """
Convert the parameterized data quality checks into a Great Expectations Expectation Suite in Python code. Each check should be represented as an expectation with appropriate parameters. Don't say anthing else in your response.

Expectation Types Reference:
-------------------------
ExpectColumnDistinctValuesToBeInSet
ExpectColumnDistinctValuesToContainSet
ExpectColumnDistinctValuesToEqualSet
ExpectColumnKLDivergenceToBeLessThan
ExpectColumnMaxToBeBetween
ExpectColumnMeanToBeBetween
ExpectColumnMedianToBeBetween
ExpectColumnMinToBeBetween
ExpectColumnMostCommonValueToBeInSet
ExpectColumnPairValuesAToBeGreaterThanB
ExpectColumnPairValuesToBeEqual
ExpectColumnPairValuesToBeInSet
ExpectColumnProportionOfNonNullValuesToBeBetween
ExpectColumnProportionOfUniqueValuesToBeBetween
ExpectColumnQuantileValuesToBeBetween
ExpectColumnStdevToBeBetween
ExpectColumnSumToBeBetween
ExpectColumnToExist
ExpectColumnUniqueValueCountToBeBetween
ExpectColumnValueLengthsToBeBetween
ExpectColumnValueLengthsToEqual
ExpectColumnValueZScoresToBeLessThan
ExpectColumnValuesToBeBetween
ExpectColumnValuesToBeDateutilParseable
ExpectColumnValuesToBeDecreasing
ExpectColumnValuesToBeInSet
ExpectColumnValuesToBeInTypeList
ExpectColumnValuesToBeIncreasing
ExpectColumnValuesToBeJsonParseable
ExpectColumnValuesToBeNull
ExpectColumnValuesToBeOfType
ExpectColumnValuesToBeUnique
ExpectColumnValuesToMatchJsonSchema
ExpectColumnValuesToMatchLikePattern
ExpectColumnValuesToMatchLikePatternList
ExpectColumnValuesToMatchRegex
ExpectColumnValuesToMatchRegexList
ExpectColumnValuesToMatchStrftimeFormat
ExpectColumnValuesToNotBeInSet
ExpectColumnValuesToNotBeNull
ExpectColumnValuesToNotMatchLikePattern
ExpectColumnValuesToNotMatchLikePatternList
ExpectColumnValuesToNotMatchRegex
ExpectColumnValuesToNotMatchRegexList
ExpectCompoundColumnsToBeUnique
ExpectMulticolumnSumToEqual
ExpectMulticolumnValuesToBeUnique
ExpectQueryResultsToMatchComparison
ExpectSelectColumnValuesToBeUniqueWithinRecord
ExpectTableColumnCountToBeBetween
ExpectTableColumnCountToEqual
ExpectTableColumnsToMatchOrderedList
ExpectTableColumnsToMatchSet
ExpectTableRowCountToBeBetween
ExpectTableRowCountToEqual
ExpectTableRowCountToEqualOtherTable

Known errors to avoid:
-------------------------
Error creating expectation ExpectColumnValuesToBeBetween: 1 validation error for ExpectColumnValuesToBeBetween
parse_strings_as_datetimes
  extra fields not permitted (type=value_error.extra)
-------------------------

Note:
* The output should be valid Python code that can be executed within a Great Expectations DataContext.
* Do not include any explanations or additional text.
* Refer to the following example output for context initialization
* In the meta parameter, put the associated check_id 
* Only use existing check_ids from the proposals provided
* You should try to create expectations for all checks where possible.
* Make you to give the correct parameters for each expectation based on the check details. If uncertain, use another expectation type that fits better.
* For freshness checks, compare against the current date.
* The suite should be named "radacct_expectation_suite"

Example output:
```
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

def safe_add_expectation(suite, expectation_fn, **kwargs):
    try:
        expectation = expectation_fn(**kwargs)
        suite.add_expectation(expectation)
        print(f"Added expectation: {{expectation.expectation_type}}")
    except Exception as e:
        print(f"Error creating expectation {{expectation_fn.__name__}}: {{e}}")

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToNotBeNull,
    meta={{"check_id": "<CHECK_ID>"}},
    column="passenger_count"
)

safe_add_expectation(
    suite,
    gx.expectations.ExpectColumnValuesToBeBetween,
    meta={{"check_id": "<CHECK_ID>"}},
    column="fare_amount",
    min_value=0,
    max_value=500
)

# ... add more using safe_add_expectation(...)

```

Here are the data quality checks to convert:
{proposals}

Output:
"""