import duckdb

# Connect to your database
conn = duckdb.connect('moma_analytics.duckdb')

# Print the tables to the terminal
print("Tables found in DB:")
print(conn.execute("SHOW TABLES").df())