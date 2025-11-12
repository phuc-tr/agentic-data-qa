PROMPT_TEMPLATE = """
Convert the parameterized data quality checks into a Great Expectations Expectation Suite in JSON format. Each check should be represented as an expectation with appropriate parameters.

Example output:
{{
  "name": "my_expectation_suite",
  "expectations": [
    {{
      "type": "expect_column_values_to_be_between",
      "kwargs": {{
        "column": "age",
        "min_value": 0,
        "max_value": 120
      }}
    }},
    {{
      "type": "expect_column_values_to_not_be_null",
      "kwargs": {{
        "column": "name"
      }}
    }}
  ]
}}

Here are the data quality checks to convert:
{proposals}

Output:
"""