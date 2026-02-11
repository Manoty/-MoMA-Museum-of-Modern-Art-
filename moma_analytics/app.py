import streamlit as st
import pandas as pd
import duckdb

st.set_page_config(page_title="MoMA Analytics", layout="wide")
st.title("🎨 MoMA Collection Analytics")
st.markdown("*Powered by dbt + DuckDB*")

conn = duckdb.connect('moma_analytics.duckdb')

# Load all data
dim_artist = conn.execute("SELECT * FROM dim_artist").df()
dim_artwork = conn.execute("SELECT * FROM dim_artwork").df()
fct = conn.execute("SELECT * FROM fct_artwork_acquisition").df()
agg_year_nat = conn.execute("SELECT * FROM agg_acquisitions_by_year_nationality").df()
agg_medium = conn.execute("SELECT * FROM agg_by_medium").df()
agg_decade = conn.execute("SELECT * FROM agg_by_decade").df()
agg_artists = conn.execute("SELECT * FROM agg_top_artists").df()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Summary", "📈 Trends", "🎨 Medium", "👥 Top Artists", "👤 Demographics"])

with tab1:
    st.subheader("Collection Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Artworks", len(dim_artwork))
    col2.metric("Total Artists", len(dim_artist))
    col3.metric("Living Artists", int(dim_artist['is_living'].sum()))
    col4.metric("Avg Artwork Area", f"{dim_artwork['area_cm2'].mean():.0f} cm²")
    
    st.markdown("---")
    
    st.subheader("Artists by Gender")
    gender_counts = dim_artist['Gender'].value_counts()
    st.bar_chart(gender_counts)
    
    st.subheader("Living vs Deceased")
    living_counts = dim_artist['is_living'].value_counts()
    st.bar_chart(living_counts)

with tab2:
    st.subheader("Acquisitions Over Time")
    agg_by_year = agg_year_nat.groupby('acquisition_year')['artwork_count'].sum().sort_index()
    st.bar_chart(agg_by_year)
    
    st.markdown("---")
    
    st.subheader("Acquisitions by Decade")
    decade_chart = agg_decade.set_index('decade')['artwork_count'].sort_index()
    st.bar_chart(decade_chart)
    
    st.markdown("---")
    
    st.subheader("Top 10 Nationalities")
    top_nat = agg_year_nat.groupby('artist_nationality')['artwork_count'].sum().nlargest(10).sort_values()
    st.bar_chart(top_nat)

with tab3:
    st.subheader("🎨 Analysis 1: Medium/Technique Popularity")
    st.markdown("**What materials/techniques does MoMA collect most?**")
    
    st.subheader("Top 20 Mediums by Count")
    top_mediums = agg_medium.head(20)[['Medium', 'artwork_count']].set_index('Medium')
    st.bar_chart(top_mediums)
    
    st.subheader("Medium Statistics Table")
    st.dataframe(agg_medium.head(30), width='stretch')

with tab4:
    st.subheader("👥 Analysis 2: Top Artists by Productivity")
    st.markdown("**Which artists have the most works in the collection?**")
    
    st.subheader("Top 20 Artists by Artwork Count")
    top_artists = agg_artists.head(20)[['artist_name', 'artwork_count']].set_index('artist_name')
    st.bar_chart(top_artists)
    
    st.subheader("Artist Productivity Table")
    st.dataframe(agg_artists.head(50), width='stretch')

with tab5:
    st.subheader("📊 Analysis 3: Acquisition Rate Trends")
    st.markdown("**How has acquisition rate changed over decades?**")
    
    st.subheader("Artworks Acquired per Decade")
    decade_data = agg_decade[['decade', 'artwork_count']].set_index('decade')
    st.bar_chart(decade_data)
    
    st.subheader("Decade Statistics")
    st.dataframe(agg_decade, width='stretch')

st.markdown("---")
st.success("✅ All 3 analyses loaded: Medium Analysis | Artist Productivity | Acquisition Rate Trends")