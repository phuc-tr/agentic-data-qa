from datetime import datetime
import json
import yaml
import sqlalchemy
import pandas as pd
import numpy as np

def main():
    with open("configs/datasources.yaml", "r") as f:
        datasources = yaml.safe_load(f)
    dataset = "raddb"
    raddb_conf = datasources[dataset]
    uri = (
        f"mysql+pymysql://{raddb_conf['username']}:{raddb_conf['password']}@"
        f"{raddb_conf['host']}:{raddb_conf['port']}/{raddb_conf['database']}"
    )
    print(uri)

    engine = sqlalchemy.create_engine(uri)

    test_query = "SELECT * FROM radacct LIMIT 10;"
    df_test = pd.read_sql(test_query, engine)
    print(df_test.head())

    run_id = datetime.now().strftime("%Y%m%d%H%M%S")
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

    sample_path = f"artifacts/samples/{dataset}.{run_id}.parquet"
    df.to_parquet(sample_path, index=False)
    print(f"Sample saved to {sample_path}")

    profile = {
        "row_count": len(df),
        "null_rate": df.isnull().mean().to_dict(),
        "distinct_ratio": {c: df[c].nunique() / len(df) for c in df.columns},
        "p01": df.quantile(0.01, numeric_only=True).to_dict(),
        "p99": df.quantile(0.99, numeric_only=True).to_dict(),
        "topk": {
            c: {str(k): v for k, v in df[c].value_counts(dropna=False).head(5).items()}
            for c in df.columns
        },
        "freshness_days": (datetime.now() - pd.to_datetime(df["acctstarttime"].max())).days,
    }

    profile_path = f"artifacts/profiles/{dataset}.{run_id}.json"
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"Profile saved to {profile_path}")

if __name__ == "__main__":
    main()
