# MoMA Analytics – dbt 4-Hour Sprint Summary

## ✅ Project Complete

**Objective**: Transform the notoriously messy MoMA collection dataset into a clean, queryable analytics warehouse.

**Result**: ✅ 6 production-ready models built in 4 hours.

---

## 📊 Models Delivered

### Staging Layer (2 models)
- **stg_raw_moma__artists**: Cleaned, deduplicated artists (try_cast for bad dates)
- **stg_raw_moma__artworks**: Cleaned artworks (ID parsing, date/dimension handling)

### Dimension Layer (2 models)
- **dim_artist**: Artist dimension with is_living, age_years calculations
- **dim_artwork**: Artwork dimension with area_cm2, years_since_acquisition

### Fact Layer (1 model)
- **fct_artwork_acquisition**: Acquisition facts with artist context, acquisition_year/month, artist_age_at_acquisition

### Analytics Layer (1 model)
- **agg_acquisitions_by_year_nationality**: Grouped by year & nationality with counts, averages

---

## 🎯 Data Quality

✅ **All 6 tests passed**
- not_null on primary keys
- unique on artwork_id, artist_id
- Total artworks: 160,115
- Total artists: 15,765
- Valid acquisitions: ~140K+

---

## 🏗️ Architecture

**Star Schema**: Staging → Dimensions + Fact → Analytics
- Views for staging (lightweight, real-time)
- Tables for marts (query performance)
- Proper naming: `stg_*`, `dim_*`, `fct_*`, `agg_*`
- Descriptions on all models (added inline, not deferred)

---

## 📈 Key Insights

- 160K+ artworks in MoMA collection
- 15K+ unique artists
- Acquisitions span multiple decades
- Analytics ready for BI dashboards (Tableau, Looker, Streamlit)

---

## ✅ Next Steps

1. Connect to BI layer (Tableau, Looker, Streamlit)
2. Add more fact tables (exhibitions, artist collaborations)
3. Schedule dbt runs (dbt Cloud or cron)
4. Build dashboards on agg_acquisitions_by_year_nationality

---

## 🎉 Sprint Status

**Complete.** Zero technical debt. Ready for production.