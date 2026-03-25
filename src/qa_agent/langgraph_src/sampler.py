from datetime import datetime
import json
import yaml
import sqlalchemy
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np


def get_schema_view(engine, table_name: str, table: pa.Table) -> dict:
    """
    Returns schema metadata comparing declared DB types vs observed pyarrow types.
    """
    insp = sqlalchemy.inspect(engine)
    declared_types = {
        col["name"]: str(col["type"])
        for col in insp.get_columns(table_name)
    }
    observed_types = {field.name: str(field.type) for field in table.schema}

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

        # Execute query and convert to pyarrow Table
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            columns = result.keys()
            rows = result.fetchall()

        # Convert to pyarrow Table with type safety
        data_dict = {col: [] for col in columns}
        for row in rows:
            for i, col in enumerate(columns):
                data_dict[col].append(row[i])
        
        try:
            # Try to infer types from data
            table = pa.table(data_dict)
        except (pa.ArrowTypeError, pa.ArrowInvalid, TypeError) as e:
            print(f"Warning: Type inference failed for {table_name}, converting to strings: {e}")
            # Fallback: convert all values to strings
            safe_dict = {}
            for col, values in data_dict.items():
                safe_dict[col] = [str(v) if v is not None else None for v in values]
            table = pa.table(safe_dict)

        # Save sample using pyarrow parquet with error handling
        sample_path = f"artifacts/samples/{dataset}.{table_name}.{run_id}.parquet"
        try:
            pq.write_table(table, sample_path)
            print(f"Sample saved to {sample_path}")
        except Exception as e:
            print(f"Error writing parquet for {table_name}: {e}")
            # Fallback: try converting all columns to string type
            safe_table = table.select([
                pa.compute.cast(table[col], pa.string()) if not pa.types.is_string(table[col].type) 
                else table[col]
                for col in table.column_names
            ])
            pq.write_table(safe_table, sample_path)
            print(f"Sample saved to {sample_path} (with string conversion)")

        # Build profile
        profile = {
            "row_count": len(table),
            "null_rate": {},
            "distinct_ratio": {},
            "p01": {},
            "p99": {},
        }
        
        for col in table.column_names:
            try:
                col_data = table.column(col)
                # Null rate
                null_count = col_data.null_count
                profile["null_rate"][col] = float(null_count) / len(table)
                
                # Distinct ratio (safe compute)
                try:
                    unique_vals = pa.compute.unique(col_data)
                    distinct_count = int(pa.compute.count(unique_vals))
                    profile["distinct_ratio"][col] = float(distinct_count) / len(table)
                except Exception as e:
                    print(f"Warning: Could not compute distinct ratio for {col}: {e}")
                    profile["distinct_ratio"][col] = None
                    
            except Exception as e:
                print(f"Warning: Error processing column {col}: {e}")
                profile["null_rate"][col] = None
                profile["distinct_ratio"][col] = None

        # Add quantiles for numeric columns only
        for col in table.column_names:
            col_data = table.column(col)
            # Only compute quantiles for integer or float types
            if pa.types.is_integer(col_data.type) or pa.types.is_floating(col_data.type):
                try:
                    # Filter out nulls and get sorted values
                    valid_mask = pa.compute.invert(pa.compute.is_null(col_data))
                    valid_data = pa.compute.filter(col_data, valid_mask)
                    if len(valid_data) > 0:
                        sorted_indices = pa.compute.sort_indices(valid_data)
                        idx_01 = max(0, int(len(valid_data) * 0.01) - 1)
                        idx_99 = min(len(valid_data) - 1, int(len(valid_data) * 0.99))
                        p01_idx = int(sorted_indices[idx_01].as_py())
                        p99_idx = int(sorted_indices[idx_99].as_py())
                        profile["p01"][col] = float(valid_data[p01_idx].as_py())
                        profile["p99"][col] = float(valid_data[p99_idx].as_py())
                except Exception as e:
                    print(f"Warning: Could not compute quantiles for {col}: {e}")
                    profile["p01"][col] = None
                    profile["p99"][col] = None

        combined_profiles[table_name] = profile

        # Schema Metadata
        try:
            schema_metadata = get_schema_view(engine, table_name, table)
            combined_schemas[table_name] = schema_metadata
        except Exception as e:
            print(f"Warning: Could not generate schema metadata for {table_name}: {e}")
            combined_schemas[table_name] = {"error": str(e)}

    # Save combined profiles
    profile_path = f"artifacts/profiles/{dataset}.{run_id}.json"
    try:
        with open(profile_path, "w") as f:
            json.dump(combined_profiles, f, indent=2, default=str)
        print(f"Profiles saved to {profile_path}")
    except Exception as e:
        print(f"Error saving profiles to {profile_path}: {e}")

    # Save combined schemas
    schema_path = f"artifacts/metadata/{dataset}.schema_view.{run_id}.json"
    try:
        with open(schema_path, "w") as f:
            json.dump(combined_schemas, f, indent=2, default=str)
        print(f"Schemas saved to {schema_path}")
    except Exception as e:
        print(f"Error saving schemas to {schema_path}: {e}")


if __name__ == "__main__":
    # Example:
    # main(dataset="raddb", data_contract="contracts/raddb.yaml")
    pass
