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


def get_first_table_name(contract: dict) -> str:
    """
    Return the first model key from the data contract.
    """
    models = contract.get("models")
    if not models:
        raise ValueError("No models defined in data contract")
    return next(iter(models.keys()))


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

    # Take first model as table name
    table_name = get_first_table_name(contract)

    seed = 42
    np.random.seed(seed)
    sampling_rule = "time_window"

    if sampling_rule == "hash_mod":
        query = (
            f"SELECT * FROM {table_name} "
            f"WHERE MOD({table_name}id, 100) = 0 LIMIT 100;"
        )
    elif sampling_rule == "time_window":
        query = (
            f"SELECT * FROM {table_name} "
            f"ORDER BY acctstarttime DESC LIMIT 100;"
        )
    else:
        raise ValueError(f"Unknown sampling rule: {sampling_rule}")

    df = pd.read_sql(query, engine)

    # Save sample
    sample_path = f"artifacts/samples/{dataset}.{run_id}.parquet"
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
        "freshness_days": (
            datetime.now()
            - pd.to_datetime(df["acctstarttime"].max())
        ).days,
    }

    profile_path = f"artifacts/profiles/{dataset}.{run_id}.json"
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"Profile saved to {profile_path}")

    # Schema Metadata
    schema_metadata = get_schema_view(engine, table_name, df)
    schema_path = f"artifacts/metadata/{dataset}.schema_view.{run_id}.json"
    with open(schema_path, "w") as f:
        json.dump(schema_metadata, f, indent=2)
    print(f"Schema metadata saved to {schema_path}")


if __name__ == "__main__":
    # Example:
    # main(dataset="raddb", data_contract="contracts/raddb.yaml")
    pass
