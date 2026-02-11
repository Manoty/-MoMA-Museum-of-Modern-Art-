import streamlit as st
import pandas as pd
import duckdb

st.set_page_config(page_title="MoMA Analytics", layout="wide")
st.title("🎨 MoMA Collection Analytics")
st.markdown("*Powered by dbt + DuckDB*")

# Connect to DuckDB
conn = duckdb.connect('moma_analytics.duckdb')

# Load data
@st.cache_data
def load_data():
    dim_artist = conn.execute("SELECT * FROM dim_artist").df()
    dim_artwork = conn.execute("SELECT * FROM dim_artwork").df()
    fct = conn.execute("SELECT * FROM fct_artwork_acquisition").df()
    agg = conn.execute("SELECT * FROM agg_acquisitions_by_year_nationality").df()
    return dim_artist, dim_artwork, fct, agg

dim_artist, dim_artwork, fct, agg = load_data()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📈 Trends", "👤 Artists", "🖼️ Artworks"])

with tab1:
    st.subheader("Collection Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Artworks", len(dim_artwork))
    col2.metric("Total Artists", len(dim_artist))
    col3.metric("Living Artists", dim_artist['is_living'].sum())
    col4.metric("Avg Artwork Area", f"{dim_artwork['area_cm2'].mean():.0f} cm²")

with tab2:
    st.subheader("Acquisitions by Year & Nationality")
    st.dataframe(agg.head(20), use_container_width=True)
    
    # Chart
    agg_by_year = agg.groupby('acquisition_year')['artwork_count'].sum().sort_index()
    st.bar_chart(agg_by_year)

with tab3:
    st.subheader("Artists (Top 20 by Age)")
    st.dataframe(dim_artist.nlargest(20, 'age_years')[['artist_name', 'Nationality', 'age_years', 'is_living']], use_container_width=True)

with tab4:
    st.subheader("Artworks (Top 20 by Area)")
    st.dataframe(dim_artwork.nlargest(20, 'area_cm2')[['artwork_title', 'Medium', 'height_cm', 'width_cm', 'area_cm2']], use_container_width=True)

st.markdown("---")
st.success("✅ Dashboard loaded successfully from dbt models!")