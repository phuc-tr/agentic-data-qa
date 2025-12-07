from src import utils

PROMPT = """You are an expert data quality engineer reviewing expectation suite updates.

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

CODE_PROMPT = """Given the data contract and expectation suite, provide the improved expectation suite code.

Data Contract:
{contract}

Latest Expectation Suite Code:
{latest_code}

New Expectation Snippet:
{expectation_snippets}

Provide only the updated code, no JSON or explanation.

Updated code:
"""



def main(run_id: str):
    dataset = "raddb"

    with open(f"expectations/{dataset}_suite.py", "r") as f:
        expectation_suite = f.read()

    data_contract = utils.get_data_contract(filepath=f"contracts/contract.{dataset}.yaml")
    latest_code = utils.get_latest_expectation_suite(filepath=f"expectations/{dataset}_suite.py") 
    
    # First call: get decision
    decision_prompt = PROMPT.format(
        contract=data_contract,
        latest_code=latest_code,
        expectation_snippets=expectation_suite
    )
    
    response = utils.make_openrouter_request(decision_prompt)
    decision = utils.extract_json(response)
    
    if decision.get("update_needed"):
        # Second call: get updated code
        print("ℹ️ Update needed, generating updated expectation suite...")
        code_prompt = CODE_PROMPT.format(
            contract=data_contract,
            latest_code=latest_code,
            expectation_snippets=expectation_suite
        )
        
        code_response = utils.make_openrouter_request(code_prompt)
        updated_code = utils.extract_python_code(code_response)
        
        with open(f"expectations/{dataset}_suite.py", "w") as f:
            f.write(updated_code)
        print(f"✅ Expectation suite updated for {dataset} dataset.")
        return 1
    else:
        print(f"ℹ️ No update needed for {dataset} dataset.")
        return 0