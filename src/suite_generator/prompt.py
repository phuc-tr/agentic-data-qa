PROMPT_TEMPLATE = """
Convert the parameterized data quality checks into a Great Expectations Expectation Suite in Python code. Each check should be represented as an expectation with appropriate parameters. Don't say anthing else in your response.

Note: You must use the correct expectation type for each check. The list of types you can choose from are:
ExpectColumnDistinctValuesToBeInSet,
ExpectColumnDistinctValuesToContainSet,
ExpectColumnDistinctValuesToEqualSet,
ExpectColumnKLDivergenceToBeLessThan,
ExpectColumnMaxToBeBetween,
ExpectColumnMeanToBeBetween,
ExpectColumnMedianToBeBetween,
ExpectColumnMinToBeBetween,
ExpectColumnMostCommonValueToBeInSet,
ExpectColumnPairValuesAToBeGreaterThanB,
ExpectColumnPairValuesToBeEqual,
ExpectColumnPairValuesToBeInSet,
ExpectColumnProportionOfNonNullValuesToBeBetween,
ExpectColumnProportionOfUniqueValuesToBeBetween,
ExpectColumnQuantileValuesToBeBetween,
ExpectColumnStdevToBeBetween,
ExpectColumnSumToBeBetween,
ExpectColumnToExist,
ExpectColumnUniqueValueCountToBeBetween,
ExpectColumnValueLengthsToBeBetween,
ExpectColumnValueLengthsToEqual,
ExpectColumnValuesToBeBetween,
ExpectColumnValuesToBeDateutilParseable,
ExpectColumnValuesToBeDecreasing,
ExpectColumnValuesToBeIncreasing,
ExpectColumnValuesToBeInSet,
ExpectColumnValuesToBeInTypeList,
ExpectColumnValuesToBeJsonParseable,
ExpectColumnValuesToBeNull,
ExpectColumnValuesToBeOfType,
ExpectColumnValuesToBeUnique,
ExpectColumnValuesToMatchJsonSchema,
ExpectColumnValuesToMatchLikePattern,
ExpectColumnValuesToMatchLikePatternList,
ExpectColumnValuesToMatchRegex,
ExpectColumnValuesToMatchRegexList,
ExpectColumnValuesToMatchStrftimeFormat,
ExpectColumnValuesToNotBeInSet,
ExpectColumnValuesToNotBeNull,
ExpectColumnValuesToNotMatchLikePattern,
ExpectColumnValuesToNotMatchLikePatternList,
ExpectColumnValuesToNotMatchRegex,
ExpectColumnValuesToNotMatchRegexList,
ExpectColumnValueZScoresToBeLessThan,
ExpectCompoundColumnsToBeUnique,
ExpectMulticolumnSumToEqual,
ExpectMulticolumnValuesToBeUnique,

ExpectSelectColumnValuesToBeUniqueWithinRecord,
ExpectTableColumnCountToBeBetween,
ExpectTableColumnCountToEqual,
ExpectTableColumnsToMatchOrderedList,
ExpectTableColumnsToMatchSet,
ExpectTableRowCountToBeBetween,
ExpectTableRowCountToEqual,
ExpectTableRowCountToEqualOtherTable,
UnexpectedRowsExpectation,

Note:
The output should be valid Python code that can be executed within a Great Expectations DataContext.
Do not include any explanations or additional text.
Refer to the following example output for context initialization
In the meta parameter, put the associated check_id 

Example output:
```
import great_expectations as gx
context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

expectation = gx.expectations.ExpectColumnValuesToNotBeNull(meta={{"check_id": <CHECK_ID>}}, column="passenger_count")
suite.add_expectation(expectation)

expectation = gx.expectations.ExpectColumnValuesToBeBetween(meta={{"check_id": <CHECK_ID>}},column="fare_amount", min_value=0, max_value=500)
suite.add_expectation(expectation)
# ... add more expectations as needed
```

Here are the data quality checks to convert:
{proposals}

Output:
"""