import great_expectations as gx
import pandas as pd
import json

def main(run_id, dataset="raddb"):
    df = pd.read_parquet(f"artifacts/samples/{dataset}.{run_id}.parquet")

    context = gx.get_context()

    with open(f"expectations/{dataset}_suite.py", "r") as f:
        suite_json = json.load(f)

    suite = gx.core.ExpectationSuite(
        name=suite_json["name"],
        expectations=suite_json["expectations"]
    )

    datasource = context.data_sources.add_pandas(name="my_pandas_datasource")
    data_asset = datasource.add_dataframe_asset(name="pd_dataframe_asset")

    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch_definition")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    results = batch.validate(suite)

    output_path = f"artifacts/sandbox/{dataset}.{run_id}.report.json"
    with open(output_path, "w") as f:
        json.dump(results.to_json_dict(), f, indent=2)

    print(f"✅ Validation report saved to {output_path}")

    # Save unexpected rows
    unexpected_rows = []
    for result in results['results']:
        unexpected_rows.extend(result['result']['partial_unexpected_index_list'])

    unexpected_df = df.iloc[unexpected_rows]
    failing_path = f"artifacts/failing_examples/{dataset}.{run_id}.csv"
    unexpected_df.head(5).to_csv(failing_path, index=False)

    print(f"✅ Failing examples saved to {failing_path}")
