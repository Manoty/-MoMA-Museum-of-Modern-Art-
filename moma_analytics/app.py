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
    
    st.markdown("---")
    
    # Gender distribution chart
    st.subheader("Artists by Gender")
    gender_counts = dim_artist['Gender'].value_counts()
    st.bar_chart(gender_counts)
    
    st.subheader("Living vs Deceased")
    living_counts = dim_artist['is_living'].value_counts()
    st.bar_chart(living_counts)

with tab2:
    st.subheader("Acquisitions Over Time")
    
    # Acquisitions by year
    agg_by_year = agg.groupby('acquisition_year')['artwork_count'].sum().sort_index()
    st.bar_chart(agg_by_year)
    
    st.markdown("---")
    
    # Top nationalities
    st.subheader("Top 10 Nationalities by Acquisitions")
    top_nat = agg.groupby('artist_nationality')['artwork_count'].sum().nlargest(10).sort_values()
    st.bar_chart(top_nat)
    
    st.markdown("---")
    
    st.subheader("Detailed Year & Nationality Data")
    st.dataframe(agg.sort_values('acquisition_year', ascending=False).head(30), use_container_width=True)

with tab3:
    st.subheader("Artist Demographics")
    
    # Age distribution
    st.subheader("Age Distribution of Artists")
    age_data = dim_artist['age_years'].value_counts().sort_index()
    st.bar_chart(age_data)
    
    st.markdown("---")
    
    # Top nationalities
    st.subheader("Top 15 Nationalities (Artists)")
    nat_counts = dim_artist['Nationality'].value_counts().head(15)
    st.bar_chart(nat_counts)
    
    st.markdown("---")
    st.subheader("Top 20 Artists (by Age)")
    st.dataframe(dim_artist.nlargest(20, 'age_years')[['artist_name', 'Nationality', 'age_years', 'is_living']], use_container_width=True)

with tab4:
    st.subheader("Artwork Dimensions Analysis")
    
    # Height distribution
    st.subheader("Height Distribution (cm)")
    height_data = dim_artwork['height_cm'].value_counts().sort_index()
    st.bar_chart(height_data.head(50))
    
    st.markdown("---")
    
    # Width distribution
    st.subheader("Width Distribution (cm)")
    width_data = dim_artwork['width_cm'].value_counts().sort_index()
    st.bar_chart(width_data.head(50))
    
    st.markdown("---")
    st.subheader("Top 20 Largest Artworks")
    st.dataframe(dim_artwork.nlargest(20, 'area_cm2')[['artwork_title', 'Medium', 'height_cm', 'width_cm', 'area_cm2']], use_container_width=True)

st.markdown("---")
st.success("✅ Dashboard loaded successfully from dbt models!")