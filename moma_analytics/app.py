import streamlit as st
import pandas as pd
import duckdb

st.set_page_config(page_title="MoMA Analytics", layout="wide")
st.title("🎨 MoMA Collection Analytics")
st.markdown("*Powered by dbt + DuckDB*")

# Connect to DuckDB
conn = duckdb.connect('moma_analytics.duckdb')

# Load data with error handling
@st.cache_data
def load_data():
    try:
        dim_artist = conn.execute("SELECT * FROM dim_artist").df()
        dim_artwork = conn.execute("SELECT * FROM dim_artwork").df()
        fct = conn.execute("SELECT * FROM fct_artwork_acquisition").df()
        agg_year_nat = conn.execute("SELECT * FROM agg_acquisitions_by_year_nationality").df()
        
        # Try to load new tables, catch errors
        try:
            agg_medium = conn.execute("SELECT * FROM agg_by_medium").df()
        except:
            st.warning("agg_by_medium table not found")
            agg_medium = pd.DataFrame()
        
        try:
            agg_decade = conn.execute("SELECT * FROM agg_by_decade").df()
        except:
            st.warning("agg_by_decade table not found")
            agg_decade = pd.DataFrame()
        
        try:
            agg_artists = conn.execute("SELECT * FROM agg_top_artists").df()
        except:
            st.warning("agg_top_artists table not found")
            agg_artists = pd.DataFrame()
        
        return dim_artist, dim_artwork, fct, agg_year_nat, agg_medium, agg_decade, agg_artists
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None, None, None

dim_artist, dim_artwork, fct, agg_year_nat, agg_medium, agg_decade, agg_artists = load_data()

# Check if data loaded
if dim_artist is None:
    st.error("Failed to load data. Check your DuckDB connection.")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Summary", "📈 Trends", "🎨 Medium", "👥 Top Artists", "👤 Demographics"])

with tab1:
    st.subheader("Collection Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Artworks", len(dim_artwork))
    col2.metric("Total Artists", len(dim_artist))
    col3.metric("Living Artists", dim_artist['is_living'].sum())
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
    
    if not agg_decade.empty:
        st.subheader("Acquisitions by Decade")
        decade_chart = agg_decade.set_index('decade')['artwork_count']
        st.bar_chart(decade_chart)
    
    st.markdown("---")
    
    st.subheader("Top 10 Nationalities by Acquisitions")
    top_nat = agg_year_nat.groupby('artist_nationality')['artwork_count'].sum().nlargest(10).sort_values()
    st.bar_chart(top_nat)
    
    st.markdown("---")
    
    st.subheader("Detailed Year & Nationality Data")
    st.dataframe(agg_year_nat.sort_values('acquisition_year', ascending=False).head(30), width='stretch')

with tab3:
    st.subheader("Analysis 1: Medium/Technique Popularity")
    
    st.markdown("**What materials/techniques does MoMA collect most?**")
    
    st.write(f"Loaded {len(agg_medium)} mediums")
    
    if len(agg_medium) > 0:
        st.subheader("Top 15 Mediums by Count")
        top_med = agg_medium.head(15)
        st.write(top_med)
        
        chart_data = top_med[['Medium', 'artwork_count']].set_index('Medium')
        st.bar_chart(chart_data)
    else:
        st.error("No medium data loaded")
with tab4:
    st.subheader("Analysis 2: Artist Productivity - Top Artists")
    
    st.markdown("**Which artists have the most works in the collection?**")
    
    if not agg_artists.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 20 Artists by Artwork Count")
            top_artists_chart = agg_artists.head(20).set_index('artist_name')['artwork_count']
            st.bar_chart(top_artists_chart)
        
        with col2:
            st.subheader("Top 20 Artists by Medium Diversity")
            artist_diversity = agg_artists.nlargest(20, 'medium_types').set_index('artist_name')['medium_types']
            st.bar_chart(artist_diversity)
        
        st.markdown("---")
        st.subheader("Full Artist Productivity Data")
        st.dataframe(agg_artists.head(50)[['artist_name', 'artist_nationality', 'artwork_count', 'medium_types', 'first_acquired', 'last_acquired', 'years_span']], width='stretch')
    else:
        st.warning("Artist productivity data not available")

with tab5:
    st.subheader("Artist Demographics")
    
    st.subheader("Age Distribution of Artists")
    age_data = dim_artist['age_years'].value_counts().sort_index()
    st.bar_chart(age_data)
    
    st.markdown("---")
    
    st.subheader("Top 15 Nationalities (Artists)")
    nat_counts = dim_artist['Nationality'].value_counts().head(15)
    st.bar_chart(nat_counts)
    
    st.markdown("---")
    st.subheader("Top 20 Artists (by Age)")
    st.dataframe(dim_artist.nlargest(20, 'age_years')[['artist_name', 'Nationality', 'age_years', 'is_living']], width='stretch')

st.markdown("---")
st.success("✅ Dashboard loaded with analyses!")