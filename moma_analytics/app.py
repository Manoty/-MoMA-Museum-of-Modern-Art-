import streamlit as st
import duckdb

st.set_page_config(page_title="MoMA Analytics", layout="wide")
st.title("🎨 MoMA Collection Analytics")
st.markdown("*Powered by dbt + DuckDB*")

conn = duckdb.connect('moma_analytics.duckdb')

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Summary", "📈 Trends", "🎨 Medium", "👥 Artists", "📊 Decade"])

with tab1:
    st.subheader("Collection Overview")
    
    dim_artist = conn.execute("SELECT * FROM dim_artist").df()
    dim_artwork = conn.execute("SELECT * FROM dim_artwork").df()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Artworks", len(dim_artwork))
    col2.metric("Total Artists", len(dim_artist))
    col3.metric("Living Artists", int(dim_artist['is_living'].sum()))
    col4.metric("Avg Artwork Area", f"{dim_artwork['area_cm2'].mean():.0f} cm²")
    
    st.markdown("---")
    st.subheader("Artists by Gender")
    gender_counts = dim_artist['Gender'].value_counts()
    st.bar_chart(gender_counts)

with tab2:
    st.subheader("Acquisitions Over Time")
    
    agg_year_nat = conn.execute("SELECT * FROM agg_acquisitions_by_year_nationality").df()
    
    agg_by_year = agg_year_nat.groupby('acquisition_year')['artwork_count'].sum().sort_index()
    st.bar_chart(agg_by_year)
    
    st.markdown("---")
    st.subheader("Top 10 Nationalities")
    top_nat = agg_year_nat.groupby('artist_nationality')['artwork_count'].sum().nlargest(10).sort_values()
    st.bar_chart(top_nat)

with tab3:
    st.subheader("🎨 Medium/Technique Popularity")
    
    agg_medium = conn.execute("SELECT * FROM agg_by_medium").df()
    
    st.subheader("Top 20 Mediums by Count")
    top_med = agg_medium.head(20)[['Medium', 'artwork_count']].set_index('Medium')
    st.bar_chart(top_med)
    
    st.markdown("---")
    st.subheader("Full Medium Data")
    st.dataframe(agg_medium.head(30), width='stretch')

with tab4:
    st.subheader("👥 Top Artists by Productivity")
    
    agg_artists = conn.execute("SELECT * FROM agg_top_artists").df()
    
    st.subheader("Top 20 Artists by Artwork Count")
    top_artists = agg_artists.head(20)[['artist_name', 'artwork_count']].set_index('artist_name')
    st.bar_chart(top_artists)
    
    st.markdown("---")
    st.subheader("Full Artist Data")
    st.dataframe(agg_artists.head(50), width='stretch')

with tab5:
    st.subheader("📊 Acquisition Rate by Decade")
    
    agg_decade = conn.execute("SELECT * FROM agg_by_decade").df()
    
    st.subheader("Artworks Acquired per Decade")
    decade_data = agg_decade[['decade', 'artwork_count']].set_index('decade')
    st.bar_chart(decade_data)
    
    st.markdown("---")
    st.subheader("Full Decade Data")
    st.dataframe(agg_decade, width='stretch')

st.markdown("---")
st.success("✅ All analyses loaded!")