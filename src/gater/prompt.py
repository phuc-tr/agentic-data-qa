PROMPT_TEMPLATE = """
Filter the expectation code snippets to only include those that are marked as 'go' in the decisions JSON.
You are given:
1. A set of expectation code snippets that define various data quality checks.
2. A decisions JSON that indicates which checks should be kept ('go': true) and which should be filtered out ('go': false).
Your task is to:
- Parse the decisions JSON to identify which checks are marked as 'go'.
- Filter the expectation code snippets to only include those checks that are marked as 'go'.
Here is the decisions JSON:
{decisions_json}
Here are the expectation code snippets:
{expectation_snippets}
Provide the filtered expectation code snippets that only include those checks marked as 'go'.
Filtered Expectation Code Snippets:
"""