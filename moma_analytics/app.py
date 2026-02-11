import streamlit as st
import pandas as pd
import duckdb

st.title("Test")

conn = duckdb.connect('moma_analytics.duckdb')

st.write("Testing DuckDB connection...")

try:
    agg_medium = conn.execute("SELECT * FROM agg_by_medium LIMIT 10").df()
    st.write(f"✅ agg_by_medium loaded: {len(agg_medium)} rows")
    st.dataframe(agg_medium)
except Exception as e:
    st.error(f"❌ Error: {e}")

try:
    agg_decade = conn.execute("SELECT * FROM agg_by_decade LIMIT 10").df()
    st.write(f"✅ agg_by_decade loaded: {len(agg_decade)} rows")
    st.dataframe(agg_decade)
except Exception as e:
    st.error(f"❌ Error: {e}")

try:
    agg_artists = conn.execute("SELECT * FROM agg_top_artists LIMIT 10").df()
    st.write(f"✅ agg_top_artists loaded: {len(agg_artists)} rows")
    st.dataframe(agg_artists)
except Exception as e:
    st.error(f"❌ Error: {e}")