# MoMA Analytics - dbt + DuckDB + Streamlit

A complete analytics warehouse for the Museum of Modern Art (MoMA) collection built with dbt, DuckDB, and Streamlit.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Virtual environment (venv)

### Installation

1. Clone/download this project
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install dbt-core dbt-duckdb streamlit pandas
```

4. Initialize dbt:
```bash
dbt init moma_analytics
# Select duckdb as database
```

5. Add CSV data:
- Place `artworks.csv` and `artists.csv` in `seeds/` folder

### Build the Data Warehouse
```bash
# Load raw data
dbt seed

# Build models
dbt run

# Run tests
dbt test

# Generate docs
dbt docs generate
dbt docs serve
```

### Launch Dashboard
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📊 Dashboard Overview

**12 Interactive Analyses:**

1. **Summary** - Collection metrics & overview
2. **Trends** - Acquisitions over time
3. **Medium** - Top materials/techniques
4. **Artists** - Most productive artists
5. **Decade** - Acquisition rates by decade
6. **Nationality-Year** - Geographic trends heatmap
7. **Medium-Trends** - Which mediums were popular when
8. **Geographic** - Country-by-country diversity
9. **Artwork Size** - Size trends over time
10. **Artist Lifespan** - Lifespan vs collection presence
11. **Collection Concentration** - Pareto analysis (how many artists = X%)
12. **Decade Detail** - Detailed breakdown by decade/nationality/medium

---

## 🏗️ Data Models (14 Total)

### Staging (2)
- `stg_raw_moma__artists` - Cleaned artist data
- `stg_raw_moma__artworks` - Cleaned artwork data

### Dimensions (2)
- `dim_artist` - Artist dimension with demographics
- `dim_artwork` - Artwork dimension with measurements

### Facts (1)
- `fct_artwork_acquisition` - Complete acquisition facts

### Analytics (9)
- `agg_acquisitions_by_year_nationality`
- `agg_by_medium`
- `agg_by_decade`
- `agg_top_artists`
- `agg_nationality_by_year`
- `agg_medium_by_year`
- `agg_geographic_diversity`
- `agg_artwork_size_by_decade`
- `agg_artist_lifespan_analysis`
- `agg_collection_concentration`
- `agg_decade_detailed_breakdown`

---

## 📈 Key Insights

- **146,007** artworks in collection
- **15,765** unique artists
- Top artist: Ludwig Mies van der Rohe (14,539 works)
- Top medium: Gelatin silver print (15,463 works)
- Top country: American artists dominate
- **Pareto insight**: Top 50 artists = 50% of collection

---

## 📁 Project Structure
```
moma_analytics/
├── dbt_project.yml          # dbt config
├── models/
│   ├── sources.yml          # Data source definitions
│   ├── staging/             # Staging models (2)
│   └── marts/               # Analytics models (12)
├── seeds/
│   ├── artworks.csv         # Raw artworks data
│   └── artists.csv          # Raw artists data
├── tests/                   # Data quality tests
├── app.py                   # Streamlit dashboard
├── moma_analytics.duckdb    # DuckDB database
├── README.md                # This file
└── FINAL_REPORT.md          # Full business report
```

---

## 🧪 Testing

All models include data quality tests:
```bash
dbt test
```

Tests include:
- `not_null` on primary keys
- `unique` on IDs
- `accepted_values` on known domains

---

## 📚 Documentation

View dbt documentation:
```bash
dbt docs generate
dbt docs serve
```

Browse at `http://localhost:8000`

---

## 🚀 Next Steps

1. **Deploy to Cloud**
   - Move DuckDB to Snowflake/BigQuery
   - Deploy Streamlit to Streamlit Cloud
   - Schedule dbt runs (daily/weekly)

2. **Expand Analytics**
   - Add exhibition data
   - Artist collaboration networks
   - Price/valuation trends

3. **Add Interactivity**
   - Date range filters
   - Artist search
   - PDF report export

4. **Performance**
   - Incremental models for large datasets
   - Query caching
   - Data mart materialization

---

## 📊 Technology Stack

- **Data Transformation**: dbt 1.11.4
- **Data Warehouse**: DuckDB (local SQLite-like)
- **Dashboard**: Streamlit
- **Language**: SQL + Python
- **Testing**: dbt tests + Python

---

## 👨‍💻 Author

Built in 4-hour dbt sprint (+ extensions for extra analyses)

---

## 📝 License

Data from MoMA public dataset. Analysis for educational purposes.

---

## 📧 Support

For issues or questions, check:
- `FINAL_REPORT.md` for business insights
- dbt docs for model descriptions
- Streamlit dashboard for data exploration

---

**Status**: ✅ Production Ready | Last Updated: 2026-02-11