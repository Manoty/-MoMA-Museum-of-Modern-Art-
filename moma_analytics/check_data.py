import duckdb

conn = duckdb.connect('moma_analytics.duckdb')

print("=== agg_by_medium ===")
try:
    df = conn.execute("SELECT * FROM agg_by_medium LIMIT 5").df()
    print(df)
    print(f"Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== agg_by_decade ===")
try:
    df = conn.execute("SELECT * FROM agg_by_decade LIMIT 5").df()
    print(df)
    print(f"Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== agg_top_artists ===")
try:
    df = conn.execute("SELECT * FROM agg_top_artists LIMIT 5").df()
    print(df)
    print(f"Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"ERROR: {e}")