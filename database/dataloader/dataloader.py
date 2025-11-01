import pandas as pd
import time
from datetime import datetime
from sqlalchemy import create_engine, text

# ---- CONFIG ----
CSV_PATH = 'radacct1000000.csv'
DB_URL = 'mysql+pymysql://root:123@db/raddb'
TABLE_NAME = 'radacct'
TIME_SCALE = 0.01  # 1.0 = real-time, 0.1 = 10x faster, etc.

# ---- LOAD CSV ----
df = pd.read_csv(CSV_PATH, parse_dates=['acctstarttime'])
df = df.replace({float('nan'): ''})
df['acctinterval'] = df['acctinterval'].replace('\\N', 0)
for time_col in ['acctstarttime', 'acctupdatetime','acctstoptime']:
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
df = df.sort_values('acctstarttime').reset_index(drop=True)

def get_query(df):
    columns = df.columns.tolist()
    placeholders = ", ".join([f":{col}" for col in columns])
    col_names = ", ".join([f"`{col}`" for col in columns])
    return text(f"""
        INSERT INTO {TABLE_NAME} ({col_names})
        VALUES ({placeholders})
    """)
insert_query = get_query(df)

engine = create_engine(DB_URL)
conn = engine.connect()

prev_time = None

for acct_time, group in df.groupby('acctstarttime'):
    if prev_time is not None:
        delta = (acct_time - prev_time).total_seconds()
        print(delta)
        if delta > 0:
            print(f"[{datetime.now()}] Sleeping for {delta * TIME_SCALE} seconds")
            time.sleep(delta * TIME_SCALE)

    # Convert row to dictionary for SQLAlchemy binding
    rows = group.to_dict(orient='records')
    print(f"[{datetime.now()}] Inserting {len(rows)} rows at timestamp {acct_time}")
    # Execute insert
    try:
        conn.execute(insert_query, rows)
        conn.commit()

        print(f"[{datetime.now()}] Inserted {len(rows)} rows at timestamp {acct_time}")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting rows at timestamp {acct_time}: {e}")
    prev_time = acct_time

conn.close()
