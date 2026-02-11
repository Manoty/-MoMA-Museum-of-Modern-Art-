import duckdb

conn = duckdb.connect('moma_analytics.duckdb')

print("=== agg_by_medium ===")
result = conn.execute("""
    SELECT Medium, artwork_count, artist_count 
    FROM agg_by_medium 
    LIMIT 5
""").fetchall()
for row in result:
    print(row)

print("\n=== agg_by_decade ===")
result = conn.execute("""
    SELECT decade, artwork_count, artist_count 
    FROM agg_by_decade 
    LIMIT 5
""").fetchall()
for row in result:
    print(row)

print("\n=== agg_top_artists ===")
result = conn.execute("""
    SELECT artist_name, artwork_count, artist_nationality
    FROM agg_top_artists 
    LIMIT 5
""").fetchall()
for row in result:
    print(row)