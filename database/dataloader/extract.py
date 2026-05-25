import pandas as pd

# ---- CONFIG ----
INPUT_CSV = 'radacct1000000.csv'
OUTPUT_CSV = 'radacct_10000.csv'
N_LATEST = 10_000   # <-- change this to whatever you need

# ---- LOAD CSV ----
df = pd.read_csv(
    INPUT_CSV,
    parse_dates=['acctstarttime', 'acctupdatetime', 'acctstoptime']
)

# ---- CLEAN DATA (match previous logic) ----
df = df.replace({float('nan'): None})
df['acctinterval'] = df['acctinterval'].replace('\\N', 0)

# ---- SORT & FILTER ----
df_latest = (
    df.sort_values('acctstarttime', ascending=False)
      .head(N_LATEST)
      .sort_values('acctstarttime')  # optional: keep chronological order
)

# ---- SAVE TO CSV ----
df_latest.to_csv(OUTPUT_CSV, index=False)

print(f"Saved {len(df_latest)} latest rows to {OUTPUT_CSV}")
