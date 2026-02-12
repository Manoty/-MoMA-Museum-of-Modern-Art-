import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="MoMA Analytics", layout="wide")
st.title("🎨 MoMA Collection Analytics")
st.markdown("*Powered by dbt + DuckDB*")

conn = duckdb.connect('moma_analytics.duckdb')

# Create all 15 tabs
tabs = st.tabs([
    "📊 Summary", "📈 Trends", "🎨 Medium", 
    "👥 Artists", "📊 Decade", "🗺️ Nationality-Year", 
    "🎨 Medium-Trends", "🌍 Geographic", "📏 Artwork Size", 
    "🎓 Lifespan", "🎯 Concentration", "📋 Decade-Detail",
    "🎭 Exhibitions", "🤝 Collaborations", "💰 Valuation"
])

# Tab 1: Summary
with tabs[0]:
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

# Tab 2: Trends
with tabs[1]:
    st.subheader("Acquisitions Over Time")
    agg_year_nat = conn.execute("SELECT * FROM agg_acquisitions_by_year_nationality").df()
    agg_by_year = agg_year_nat.groupby('acquisition_year')['artwork_count'].sum().sort_index()
    st.bar_chart(agg_by_year)
    
    st.markdown("---")
    st.subheader("Top 10 Nationalities")
    top_nat = agg_year_nat.groupby('artist_nationality')['artwork_count'].sum().nlargest(10).sort_values()
    st.bar_chart(top_nat)

# Tab 3: Medium
with tabs[2]:
    st.subheader("🎨 Medium/Technique Popularity")
    agg_medium = conn.execute("SELECT * FROM agg_by_medium").df()
    
    st.subheader("Top 20 Mediums by Count")
    top_med = agg_medium.head(20)[['Medium', 'artwork_count']].set_index('Medium')
    st.bar_chart(top_med)
    
    st.markdown("---")
    st.subheader("Full Medium Data")
    st.dataframe(agg_medium.head(30), width='stretch')

# Tab 4: Artists
with tabs[3]:
    st.subheader("👥 Top Artists by Productivity")
    agg_artists = conn.execute("SELECT * FROM agg_top_artists").df()
    
    st.subheader("Top 20 Artists by Artwork Count")
    top_artists = agg_artists.head(20)[['artist_name', 'artwork_count']].set_index('artist_name')
    st.bar_chart(top_artists)
    
    st.markdown("---")
    st.subheader("Full Artist Data")
    st.dataframe(agg_artists.head(50), width='stretch')

# Tab 5: Decade
with tabs[4]:
    st.subheader("📊 Acquisition Rate by Decade")
    agg_decade = conn.execute("SELECT * FROM agg_by_decade").df()
    
    st.subheader("Artworks Acquired per Decade")
    decade_data = agg_decade[['decade', 'artwork_count']].set_index('decade')
    st.bar_chart(decade_data)
    
    st.markdown("---")
    st.subheader("Full Decade Data")
    st.dataframe(agg_decade, width='stretch')

# Tab 6: Nationality-Year
with tabs[5]:
    st.subheader("🗺️ Artist Nationality vs Acquisition Year")
    agg_nat_year = conn.execute("SELECT * FROM agg_nationality_by_year").df()
    
    st.markdown("**Heatmap: Which countries' artists were acquired when?**")
    heatmap_data = agg_nat_year.pivot_table(
        index='artist_nationality', 
        columns='acquisition_year', 
        values='artwork_count', 
        fill_value=0
    )
    
    top_nations = agg_nat_year.groupby('artist_nationality')['artwork_count'].sum().nlargest(15).index
    heatmap_filtered = heatmap_data.loc[top_nations]
    st.write(heatmap_filtered)
    
    st.markdown("---")
    st.subheader("Full Nationality-Year Data")
    st.dataframe(agg_nat_year.head(100), width='stretch')

# Tab 7: Medium-Trends
with tabs[6]:
    st.subheader("🎨 Medium Popularity Over Time")
    agg_med_year = conn.execute("SELECT * FROM agg_medium_by_year").df()
    
    st.markdown("**Which mediums were popular when?**")
    top_mediums = agg_med_year.groupby('Medium')['artwork_count'].sum().nlargest(10).index
    med_filtered = agg_med_year[agg_med_year['Medium'].isin(top_mediums)]
    
    st.subheader("Top 10 Mediums Acquisition Trend")
    for medium in top_mediums[:5]:
        med_data = med_filtered[med_filtered['Medium'] == medium].set_index('acquisition_year')['artwork_count'].sort_index()
        st.line_chart(med_data)
    
    st.markdown("---")
    st.subheader("Full Medium-Year Data")
    st.dataframe(agg_med_year.head(100), width='stretch')

# Tab 8: Geographic
with tabs[7]:
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

# Tab 9: Artwork Size
with tabs[8]:
    st.subheader("📏 Artwork Size Trends Over Time")
    agg_size = conn.execute("SELECT * FROM agg_artwork_size_by_decade").df()
    
    st.markdown("**Are newer artworks larger or smaller than old ones?**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average Artwork Area by Decade")
        size_data = agg_size[['decade', 'avg_area_cm2']].set_index('decade').sort_index()
        st.line_chart(size_data)
    
    with col2:
        st.subheader("Average Height & Width by Decade")
        hw_data = agg_size[['decade', 'avg_height_cm', 'avg_width_cm']].set_index('decade').sort_index()
        st.line_chart(hw_data)
    
    st.markdown("---")
    st.subheader("Size Trends Data")
    st.dataframe(agg_size, width='stretch')

# Tab 10: Lifespan
with tabs[9]:
    st.subheader("🎓 Artist Lifespan Analysis")
    agg_lifespan = conn.execute("SELECT * FROM agg_artist_lifespan_analysis").df()
    
    st.markdown("**How does artist lifespan relate to collection presence?**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Artists with Most Works vs Lifespan")
        lifespan_chart = agg_lifespan.nlargest(20, 'total_artworks')[['artist_name', 'lifespan_years']].set_index('artist_name')
        st.bar_chart(lifespan_chart)
    
    with col2:
        st.subheader("Avg Age at Acquisition (Top Artists)")
        age_chart = agg_lifespan.nlargest(20, 'total_artworks')[['artist_name', 'avg_age_at_acquisition']].set_index('artist_name')
        st.bar_chart(age_chart)
    
    st.markdown("---")
    st.subheader("Full Lifespan Analysis")
    st.dataframe(agg_lifespan.head(100), width='stretch')

# Tab 11: Concentration
with tabs[10]:
    st.subheader("🎯 Collection Concentration (Pareto Analysis)")
    agg_concentration = conn.execute("SELECT * FROM agg_collection_concentration").df()
    
    st.markdown("**How many artists represent X% of the collection?**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 20 Artists - Cumulative % of Collection")
        conc_chart = agg_concentration.head(20)[['artist_name', 'cumulative_pct']].set_index('artist_name')
        st.line_chart(conc_chart)
    
    with col2:
        st.subheader("Cumulative Artworks (Top 20)")
        cumul_chart = agg_concentration.head(20)[['artist_name', 'cumulative_artworks']].set_index('artist_name')
        st.line_chart(cumul_chart)
    
    st.markdown("---")
    top_50_pct = agg_concentration[agg_concentration['cumulative_pct'] <= 50].shape[0]
    top_80_pct = agg_concentration[agg_concentration['cumulative_pct'] <= 80].shape[0]
    top_90_pct = agg_concentration[agg_concentration['cumulative_pct'] <= 90].shape[0]
    
    st.subheader("Key Insights")
    col1, col2, col3 = st.columns(3)
    col1.metric("Artists for 50%", top_50_pct)
    col2.metric("Artists for 80%", top_80_pct)
    col3.metric("Artists for 90%", top_90_pct)
    
    st.markdown("---")
    st.subheader("Full Concentration Data")
    st.dataframe(agg_concentration, width='stretch')

# Tab 12: Decade-Detail
with tabs[11]:
    st.subheader("📋 Decade-by-Decade Detailed Breakdown")
    agg_decade_detail = conn.execute("SELECT * FROM agg_decade_detailed_breakdown").df()
    
    st.markdown("**Collection composition by decade, nationality, and medium**")
    decades = sorted(agg_decade_detail['decade'].unique(), reverse=True)
    selected_decade = st.selectbox("Select Decade", decades)
    
    decade_data = agg_decade_detail[agg_decade_detail['decade'] == selected_decade]
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top Nationalities ({int(selected_decade)}s)")
        nat_data = decade_data.groupby('artist_nationality')['artwork_count'].sum().nlargest(10).sort_values(ascending=True)
        st.bar_chart(nat_data)
    
    with col2:
        st.subheader(f"Top Mediums ({int(selected_decade)}s)")
        med_data = decade_data.groupby('Medium')['artwork_count'].sum().nlargest(10).sort_values(ascending=True)
        st.bar_chart(med_data)
    
    st.markdown("---")
    st.subheader(f"Detailed Data for {int(selected_decade)}s Decade")
    st.dataframe(decade_data.sort_values('artwork_count', ascending=False), width='stretch')

# Tab 13: Exhibitions
with tabs[12]:
    st.subheader("🎭 Exhibition Analysis")
    agg_exhibition = conn.execute("SELECT * FROM agg_exhibition_analysis").df()
    
    st.markdown("**Exhibition presence by nationality and medium**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 15 Nationalities in Exhibitions")
        nat_exh = agg_exhibition.groupby('artist_nationality')['artworks_in_exhibitions'].sum().nlargest(15).sort_values(ascending=True)
        st.bar_chart(nat_exh)
    
    with col2:
        st.subheader("Top 15 Mediums in Exhibitions")
        med_exh = agg_exhibition.groupby('Medium')['artworks_in_exhibitions'].sum().nlargest(15).sort_values(ascending=True)
        st.bar_chart(med_exh)
    
    st.markdown("---")
    st.subheader("Exhibition History Data")
    st.dataframe(agg_exhibition.head(50), width='stretch')

# Tab 14: Collaborations
with tabs[13]:
    st.subheader("🤝 Artist Collaboration Networks")
    agg_collab = conn.execute("SELECT * FROM agg_artist_collaborations").df()
    
    st.markdown("**Artist connections based on shared medium, nationality, and acquisition timing**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 15 Artist Pairs by Connection Score")
        collab_artists = agg_collab.nlargest(15, 'connection_score')[['artist_1_name', 'artist_2_name', 'connection_score']]
        st.dataframe(collab_artists, width='stretch')
    
    with col2:
        st.subheader("Collaboration Metrics (Top 15)")
        metrics = agg_collab.nlargest(15, 'connection_score')[['connection_score']].reset_index(drop=True)
        st.bar_chart(metrics)
    
    st.markdown("---")
    st.subheader("Full Collaboration Network")
    st.dataframe(agg_collab.head(100), width='stretch')

# Tab 15: Valuation
with tabs[14]:
    st.subheader("💰 Price/Valuation Trends")
    agg_valuation = conn.execute("SELECT * FROM agg_valuation_trends").df()
    
    st.markdown("**Valuation proxy based on acquisition patterns, artist age, and timing**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Acquisitions per Year by Decade")
        val_data = agg_valuation.groupby('decade')['avg_acquisitions_per_year'].mean().sort_index()
        st.line_chart(val_data)
    
    with col2:
        st.subheader("Valuation Tier Distribution")
        tier_counts = agg_valuation['valuation_tier'].value_counts()
        st.bar_chart(tier_counts)
    
    st.markdown("---")
    st.subheader("Detailed Valuation Analysis")
    st.dataframe(agg_valuation.head(100), width='stretch')

st.markdown("---")
st.success("✅ MoMA Analytics Dashboard - 15 Complete Analyses!")