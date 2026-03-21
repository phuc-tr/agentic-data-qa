import json
import yaml
import great_expectations as gx
import pandas as pd


def load_data_contract(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_table_names(contract: dict) -> list[str]:
    """
    Return the table names from the data contract.
    Handles both dict (keys as table names) and list (with 'name' field) formats.
    Supports 'models' or 'schema' keys.
    """
    data = contract.get("models") or contract.get("schema")
    if not data:
        raise ValueError("No models or schema defined in data contract")
    if isinstance(data, dict):
        return list(data.keys())
    elif isinstance(data, list):
        return [model["name"] for model in data]
    else:
        raise ValueError("Models/schema should be dict or list")


def validate(run_id, dataset="raddb", data_contract="contracts/contract.raddb.yaml"):
    contract = load_data_contract(data_contract)
    table_names = get_table_names(contract)

    context = gx.get_context(mode="file")
    datasource = context.data_sources.add_or_update_pandas(name="my_pandas_datasource")
    data_asset = datasource.add_dataframe_asset(name="pd_dataframe_asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch_definition")

    # Load all table samples and combine into one DataFrame
    dfs = []
    for table_name in table_names:
        path = f"artifacts/samples/{dataset}.{table_name}.{run_id}.parquet"
        dfs.append(pd.read_parquet(path))
    if not dfs:
        raise ValueError("No sample files found to validate")

    df = pd.concat(dfs, ignore_index=True)

    # Get expectation suite from context
    suite = context.suites.get("expectation_suite")

    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
    results = batch.validate(suite)

    output_path = f"artifacts/sandbox/{dataset}.{run_id}.report.json"
    with open(output_path, "w") as f:
        json.dump(results.to_json_dict(), f, indent=2)

    print(f"✅ Validation report saved to {output_path}")

    # Save unexpected rows
    unexpected_rows = []
    for result in results['results']:
        unexpected_rows.extend(result['result'].get('partial_unexpected_index_list') or [])

    unexpected_df = df.iloc[unexpected_rows]
    failing_path = f"artifacts/failing_examples/{dataset}.{run_id}.csv"
    unexpected_df.head(5).to_csv(failing_path, index=False)

    print(f"✅ Failing examples saved to {failing_path}")

    return results.to_json_dict()
