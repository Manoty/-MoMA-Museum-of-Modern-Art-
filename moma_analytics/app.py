import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="MoMA Analytics", layout="wide")
st.title("🎨 MoMA Collection Analytics")
st.markdown("*Powered by dbt + DuckDB*")

conn = duckdb.connect('moma_analytics.duckdb')

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Summary", "📈 Trends", "🎨 Medium", 
    "👥 Artists", "📊 Decade", "🗺️ Nationality-Year", 
    "🎨 Medium-Trends", "🌍 Geographic"
])

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

with tab6:
    st.subheader("🗺️ Artist Nationality vs Acquisition Year")
    
    agg_nat_year = conn.execute("SELECT * FROM agg_nationality_by_year").df()
    
    st.markdown("**Heatmap: Which countries' artists were acquired when?**")
    
    # Pivot for heatmap
    heatmap_data = agg_nat_year.pivot_table(
        index='artist_nationality', 
        columns='acquisition_year', 
        values='artwork_count', 
        fill_value=0
    )
    
    st.markdown("**Top 15 Nationalities Over Time**")
    top_nations = agg_nat_year.groupby('artist_nationality')['artwork_count'].sum().nlargest(15).index
    heatmap_filtered = heatmap_data.loc[top_nations]
    
    st.write(heatmap_filtered)
    
    st.markdown("---")
    st.subheader("Full Nationality-Year Data")
    st.dataframe(agg_nat_year.head(100), width='stretch')

with tab7:
    st.subheader("🎨 Medium Popularity Over Time")
    
    agg_med_year = conn.execute("SELECT * FROM agg_medium_by_year").df()
    
    st.markdown("**Which mediums were popular when?**")
    
    # Get top 10 mediums overall
    top_mediums = agg_med_year.groupby('Medium')['artwork_count'].sum().nlargest(10).index
    
    # Filter data for top mediums
    med_filtered = agg_med_year[agg_med_year['Medium'].isin(top_mediums)]
    
    # Chart: Top mediums over time
    st.subheader("Top 10 Mediums Acquisition Trend")
    for medium in top_mediums[:5]:
        med_data = med_filtered[med_filtered['Medium'] == medium].set_index('acquisition_year')['artwork_count'].sort_index()
        st.line_chart(med_data, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Full Medium-Year Data")
    st.dataframe(agg_med_year.head(100), width='stretch')

with tab8:
    st.subheader("🌍 Geographic Diversity Analysis")
    
    agg_geo = conn.execute("SELECT * FROM agg_geographic_diversity").df()
    
    st.markdown("**How much of the collection comes from each country?**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 20 Countries by Artworks")
        top_geo = agg_geo.head(20)[['Nationality', 'total_artworks']].set_index('Nationality')
        st.bar_chart(top_geo)
    
    with col2:
        st.subheader("Top 20 Countries by % of Collection")
        top_pct = agg_geo.head(20)[['Nationality', 'pct_of_collection']].set_index('Nationality')
        st.bar_chart(top_pct)
    
    st.markdown("---")
    st.subheader("Complete Geographic Diversity Breakdown")
    st.dataframe(agg_geo, width='stretch')

st.markdown("---")
st.success("✅ MoMA Analytics Dashboard - 8 Complete Analyses!")