from datetime import datetime
import json
import yaml
import sqlalchemy
import pandas as pd
import numpy as np


def get_schema_view(engine, table_name: str, df: pd.DataFrame) -> dict:
    """
    Returns schema metadata comparing declared DB types vs observed DataFrame types.
    """
    insp = sqlalchemy.inspect(engine)
    declared_types = {
        col["name"]: str(col["type"])
        for col in insp.get_columns(table_name)
    }
    observed_types = {c: str(dtype) for c, dtype in df.dtypes.items()}

    return {
        "declared_types": declared_types,
        "observed_types": observed_types,
    }


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


def sample(
    dataset: str,
    data_contract: str,
    run_id: str | None = None,
):
    # Use provided run_id or default to timestamp
    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d%H%M%S")

    contract = load_data_contract(data_contract)

    # Load DB credentials
    mysql_conf = contract["servers"]["mysql"]

    uri = (
        f"mysql+pymysql://{mysql_conf['username']}:{mysql_conf['password']}@"
        f"{mysql_conf['host']}:{mysql_conf['port']}/{mysql_conf['database']}"
    )

    engine = sqlalchemy.create_engine(uri)

    # Take all table names
    table_names = get_table_names(contract)
    print(f"Table names: {table_names}")

    combined_profiles = {}
    combined_schemas = {}

    for table_name in table_names:
        seed = 42
        np.random.seed(seed)
        sampling_rule = "time_window"

        if sampling_rule == "hash_mod":
            query = (
                f"SELECT * FROM {table_name} "
                f"WHERE MOD({table_name}id, 100) = 0 LIMIT 100;"
            )
        elif sampling_rule == "time_window":
            query = f"SELECT * FROM {table_name} LIMIT 100;"
        else:
            raise ValueError(f"Unknown sampling rule: {sampling_rule}")

        df = pd.read_sql(query, engine)

        # Save sample
        sample_path = f"artifacts/samples/{dataset}.{table_name}.{run_id}.parquet"
        df.to_parquet(sample_path, index=False)
        print(f"Sample saved to {sample_path}")

        # Build profile
        profile = {
            "row_count": len(df),
            "null_rate": df.isnull().mean().to_dict(),
            "distinct_ratio": {
                c: df[c].nunique() / len(df) for c in df.columns
            },
            "p01": df.quantile(0.01, numeric_only=True).to_dict(),
            "p99": df.quantile(0.99, numeric_only=True).to_dict(),
        }

        combined_profiles[table_name] = profile

        # Schema Metadata
        schema_metadata = get_schema_view(engine, table_name, df)
        combined_schemas[table_name] = schema_metadata

    # Save combined profiles
    profile_path = f"artifacts/profiles/{dataset}.{run_id}.json"
    with open(profile_path, "w") as f:
        json.dump(combined_profiles, f, indent=2)
    print(f"Profiles saved to {profile_path}")

    # Save combined schemas
    schema_path = f"artifacts/metadata/{dataset}.schema_view.{run_id}.json"
    with open(schema_path, "w") as f:
        json.dump(combined_schemas, f, indent=2)
    print(f"Schemas saved to {schema_path}")


if __name__ == "__main__":
    # Example:
    # main(dataset="raddb", data_contract="contracts/raddb.yaml")
    pass
