{{
  config(
    materialized='table',
    tags=['marts']
  )
}}

with stg_artworks as (
  select * from {{ ref('stg_raw_moma__artworks') }}
),

enriched as (
  select
    artwork_id,
    artist_id,
    artwork_title,
    Medium,
    Dimensions,
    acquisition_date,
    height_cm,
    width_cm,
    -- Calculate area for size analysis
    round((height_cm * width_cm), 2) as area_cm2,
    -- Age since acquisition (in years)
    extract(year from current_date()) - extract(year from acquisition_date) as years_since_acquisition,
    current_timestamp as dbt_loaded_at
  from stg_artworks
)

select * from enriched

-- Description: Dimension table for artworks with calculated fields (area_cm2, years_since_acquisition). One row per artwork.