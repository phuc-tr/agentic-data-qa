GENERATE_CHECKS_PROMPT_TEMPLATE = """
You are a Data Quality Engineer who writes precise, parameterized data quality checks that 
will later on be converted into quality checks, 
using frameworks such as sodacl and great expectation.

Your task:

1. Read the Data Contract, Schema, and Profile.
2. For each field defined in the contract, map them into a check type:
  - Nulls in required columns: "not_null"
  - Duplicate values in unique column: "unique"
  - Out-of-range numeric values: "range"
  - Domain/OOV category violations: "domain"
  - Freshness/staleness issues: "freshness"
  - Foreign-key mismatches: "foreign_key"
3. Prefer values explicitly defined in the contract, otherwise derive parameters from the profile  
4. In the params field, specify parameters that are helpful to be converted to quality code.
5. [params] Only when it's impossible to have numeric parameters, you can use "text" as a parameter. When doing this, avoid generic text, such as "<fieldname> must have valid value".
6. Always generate checks that are inherted from the data contract.
7. Do not make up checks that are not defined in the contract.

Below are some example outputs. Remember to refer to the provided contract and adjust the checks accordingly:

Example 1: Range check from contract
Contract:
```
price:
  ...
  quality:
    - type: text
      description: 95% of prices must be less than 300
```
Checks:
```
[
  {{
    "column": "price",
    "type": "range",
    "params": {{ "min_value": 0, "max_value": 300 }},
    "origin": "contract",
    "threshold" : ">95%"
  }}
]
```

Example 2: Missing value checks from contract
Contract:
```
properties:
  - name: email_address
    quality:
      - metric: missingValues
        arguments:
          missingValues: [null, '', 'N/A', 'n/a']
        mustBeLessThan: 5
        unit: percent
```
Checks:
```
[
  {{
    "column": "email_address",
    "type": "not_null",
    "params": {{}},
    "origin": "contract",
    "threshold" : "<5%"
  }}
]
```

Example 3: Freshness check
Contract:
```
freshness:
  threshold: 30s
  timestampField: creation_ts
```

Checks:
```
[
  {{
    "column": "creation_ts",
    "type": "freshness",
    "params": {{ "max_delay": "30s" }},
    "origin": "contract",
  }}
]
```

Example 4: Domain check
Contract:
```
country:
  quality:
    - metric: invalidValues
      arguments:
        validValues: ['US', 'DE', 'FR', 'IT']
```

Checks:
```
[
  {{
    "column": "country",
    "type": "domain",
    "params": {{ "allowed_set": ["US", "DE", "FR", "IT"] }},
    "origin": "contract",
  }}
]
```

Example 5: Value check
Contract:

```
company:
  quality:
    - type: text
      description: Must end with Inc.
```
Checks:
```
[
  {{
    "column": "company",
    "type": "domain",
    "params": {{ "text": "Must ends with Inc." }},
    "origin": "contract",
  }}
]
```

-------------------------
Here's the contract and profile:
-------------------------

Contract:
{contract}

Profile:
{profile}

Provide ONLY the JSON array of data quality checks as per the schema above.
"""

"""
2. For each field defined in the contract, only focus on those that define the quality field.
3. Generate at least one data quality check for EACH quality field in the contract.
4. Classify the quality issues such as:
   - Nulls in required columns
   - Duplicate IDs
   - Out-of-range numeric values
   - Domain/OOV category violations
   - Freshness/staleness issues
   - Foreign-key mismatches
5. For each quality defined in the contract. Map each issue to a check type:
   - "not_null"
   - "unique"
   - "range"
   - "domain"
   - "freshness"
   - "foreign_key"
6. Parameterize checks:
   - Prefer values explicitly defined in the contract
   - Otherwise derive parameters from the profile  
     (e.g., min=p01, max=p99, domain from contract, freshness SLA from profile)
7. Compute a likelihood score (0–1) using profile signals (e.g., null_rate, dup_rate, oov_rate, freshness_minutes).
8. For each check, include:
   - params
   - rationale
   - signals
   - likelihood
9. Output ONLY a JSON array matching the schema below.

-------------------------
EXAMPLE OUTPUTS
-------------------------

Example 1: Unique check derived from contract + profile  
[
  {{
    "dataset": "orders",
    "check_id": "orders:unique:order_id",
    "type": "unique",
    "column": "order_id",
    "params": {{}},
    "rationale": "Contract defines order_id as unique; profile shows dup_rate=0.0002.",
    "signals": {{ "dup_rate": 0.0002 }},
    "likelihood": 0.91,
    "origin": {{ "from_contract": true}}
  }}
]

Example 2: Domain check derived from contract with OOV detected in profile  
[
  {{
    "dataset": "orders",
    "check_id": "orders:domain:country",
    "type": "domain",
    "column": "country",
    "params": {{ "allowed_set": ["US", "DE", "FR", "IT"] }},
    "rationale": "Contract defines the allowed country list; profile shows oov_rate=0.12.",
    "signals": {{ "oov_rate": 0.12 }},
    "likelihood": 0.77,
    "origin": {{ "from_contract": true}}
  }}
]

Example 3: Range check derived from profile (no range in contract)  
[
  {{
    "dataset": "orders",
    "check_id": "orders:range:amount",
    "type": "range",
    "column": "amount",
    "params": {{ "min_value": 0, "max_value": 890 }},
    "rationale": "No contract range; use p01=0 and p99=890 from profile. Long tail to max=12840.",
    "signals": {{ "p01": 0, "p99": 890, "max": 12840 }},
    "likelihood": 0.63,
    "origin": {{ "from_contract": true}}
  }}
]

-------------------------
EXPECTED OUTPUT JSON SCHEMA
-------------------------

{{
  "type": "array",
  "items": {{
    "type": "object",
    "required": [
      "dataset",
      "check_id",
      "type",
      "column",
      "params",
      "rationale",
      "signals",
      "likelihood",
      "origin"
    ],
    "properties": {{
      "dataset": {{ "type": "string" }},

      "check_id": {{ "type": "string" }},

      "type": {{
        "type": "string",
        "enum": ["not_null", "unique", "range", "domain", "freshness", "foreign_key"]
      }},

      "column": {{ "type": "string" }},

      "params": {{
        "type": "object",
        "description": "Configuration parameters for the check"
      }},

      "rationale": {{
        "type": "string",
        "description": "Explanation of why the check is needed"
      }},

      "signals": {{
        "type": "object",
        "description": "Profile metrics used to compute the likelihood score"
      }},

      "likelihood": {{
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "description": "Risk/utility score"
      }},

      "origin": {{
        "type": "object",
        "required": ["from_contract"],
        "properties": {{
          "from_contract": {{ "type": "boolean" }}
        }}
      }}
    }}
  }}
}}

-------------------------
INPUTS
-------------------------

Contract:
{contract}

Profile:
{profile}

-------------------------
OUTPUT
-------------------------
Provide ONLY the JSON array of data quality checks as per the schema above.
"""

GENERATE_GX_SUITE_TEMPLATE = """

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
* Refer to the metadata to get the correct data type of each column

Example output:
```
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        meta={{"check_id": "<CHECK_ID>"}},
        column="passenger_count"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        meta={{"check_id": "<CHECK_ID>"}},
        column="fare_amount",
        min_value=0,
        max_value=500
    )
)

# ... add more expectations

```

Here are the data quality checks to convert:
{proposals}

Metadata for column types:
{metadata}

Output:
"""

FIX_ERROR_PROMPT = """
You are given a piece of code that contains an error.
Your task is to identify the error and fix it by rewriting the code.

Requirements:

Return the entire corrected code, not just the modified or fixed section.

Do not omit any parts of the original code unless necessary for the fix.

Ensure the corrected code is complete, consistent, and ready to run.

Do not include explanations unless explicitly asked; output only the full corrected code.

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

The begining of the code should always start with:
```
import great_expectations as gx

context = gx.get_context(mode="file")

suite_name = "radacct_expectation_suite"
suite = gx.ExpectationSuite(name=suite_name)
suite = context.suites.add(suite)
```

Code to fix:
{code}

Error:
{error_message}
"""

GATER_PROMPT = """You are an expert data quality engineer reviewing expectation suite updates.

Your task:
1. Analyze the data contract, the latest expectation suite code, and the new expectation snippet
2. Determine if updating from the latest code to the new snippet is beneficial
3. Return a JSON response with:
    - "update_needed": boolean indicating if an update should be made
    - "rationale": explanation of your decision

Data Contract:
{contract}

Latest Expectation Suite Code:
{latest_code}

New Expectation Snippet:
{expectation_snippets}

Examples:

Example 1:
Latest: expect_table_row_count_to_be_between(min_value=0, max_value=1000)
New: expect_table_row_count_to_be_between(min_value=100, max_value=10000)
Result: {{"update_needed": true, "rationale": "New snippet provides more realistic row count bounds"}}

Example 2:
Latest: expect_column_values_to_be_in_set(['A', 'B', 'C'])
New: expect_column_values_to_be_in_set(['A', 'B'])
Result: {{"update_needed": false, "rationale": "New snippet removes a valid value, would reduce coverage"}}

Example 3:
Latest: expect_column_to_exist(column_name='user_id')
New: expect_column_to_exist(column_name='user_id') AND expect_column_values_to_not_be_null(column_name='user_id')
Result: {{"update_needed": true, "rationale": "New snippet adds important null check constraint"}}

Return only valid JSON in your response.
"""

UPDATE_CODE_PROMPT = """Given the data contract and expectation suite, provide the improved expectation suite code.

Data Contract:
{contract}

Latest Expectation Suite Code:
{latest_code}

New Expectation Snippet:
{expectation_snippets}

Provide only the updated code, no JSON or explanation.

Updated code:
"""

CRAFT_PULL_REQUEST_PROMPT = """
You are an expert software engineer skilled in writing clear and concise pull request descriptions.
You will be provided with the old code (if any), the new code, and the results of validation tests of the new code.
Your task is to craft a pull request body that summarizes the changes made in the new code compared to the old code, and highlights the key results from the validation tests.

When writing the pull request body, consider including:
- A brief summary of the changes made in the new code (which new quality checks were added, modified, or removed)
- The rationale behind these changes (why were these changes necessary or beneficial)
- A summary of the validation results (how many checks passed, failed, any notable findings)
- In the notable findings section, highlight the gap between observed data and the data contract 

Old code:
{old_code}
New code:
{new_code}
Validation results:
{results}
Provide only the pull request body text in your response.
"""