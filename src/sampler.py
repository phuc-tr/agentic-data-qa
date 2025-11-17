from datetime import datetime
import json
import yaml
import sqlalchemy
import pandas as pd
import numpy as np

def get_schema_view(engine, table_name: str, df: pd.DataFrame) -> dict:
    """
    Returns schema metadata comparing declared DB types vs observed DataFrame types.
    Includes declared types, observed types, and differences.
    """
    insp = sqlalchemy.inspect(engine)
    declared_types = {col["name"]: str(col["type"]) for col in insp.get_columns(table_name)}
    observed_types = {c: str(dtype) for c, dtype in df.dtypes.items()}

    return {
        "declared_types": declared_types,
        "observed_types": observed_types,
    }


def main(run_id: str | None):
    # Use provided run_id or default to timestamp
    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d%H%M%S")

    with open("configs/datasources.yaml", "r") as f:
        datasources = yaml.safe_load(f)

    dataset = "raddb"
    raddb_conf = datasources[dataset]

    uri = (
        f"mysql+pymysql://{raddb_conf['username']}:{raddb_conf['password']}@"
        f"{raddb_conf['host']}:{raddb_conf['port']}/{raddb_conf['database']}"
    )

    engine = sqlalchemy.create_engine(uri)

    seed = 42
    np.random.seed(seed)
    sampling_rule = "time_window"

    if sampling_rule == "hash_mod":
        query = "SELECT * FROM radacct WHERE MOD(radacctid, 100) = 0 LIMIT 100;"
    elif sampling_rule == "time_window":
        query = "SELECT * FROM radacct ORDER BY acctstarttime DESC LIMIT 100;"
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
        "distinct_ratio": {c: df[c].nunique() / len(df) for c in df.columns},
        "p01": df.quantile(0.01, numeric_only=True).to_dict(),
        "p99": df.quantile(0.99, numeric_only=True).to_dict(),
        # "topk": {
        #     c: {str(k): v for k, v in df[c].value_counts(dropna=False).head(5).items()}
        #     for c in df.columns
        # },
        "freshness_days": (datetime.now() - pd.to_datetime(df["acctstarttime"].max())).days,
    }

    profile_path = f"artifacts/profiles/{dataset}.{run_id}.json"
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"Profile saved to {profile_path}")

    # Schema Metadata
    schema_metadata = get_schema_view(engine, "radacct", df)
    schema_path = f"artifacts/metadata/{dataset}.schema_view.{run_id}.json"
    with open(schema_path, "w") as f:
        json.dump(schema_metadata, f, indent=2)
    print(f"Schema metadata saved to {schema_path}")
