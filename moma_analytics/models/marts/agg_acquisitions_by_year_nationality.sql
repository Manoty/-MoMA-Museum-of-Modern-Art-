{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

agg as (
  select
    acquisition_year,
    artist_nationality,
    count(*) as artwork_count,
    count(distinct artist_id) as artist_count,
    round(avg(artist_age_at_acquisition), 1) as avg_artist_age,
    min(artist_age_at_acquisition) as min_artist_age,
    max(artist_age_at_acquisition) as max_artist_age
  from fct
  where acquisition_year is not null
    and artist_nationality is not null
  group by acquisition_year, artist_nationality
)

select
  acquisition_year,
  artist_nationality,
  artwork_count,
  artist_count,
  avg_artist_age,
  min_artist_age,
  max_artist_age
from agg
order by acquisition_year desc, artwork_count desc

-- Description: Analytics mart aggregating acquisitions by year and artist nationality. Supports trend and diversity analysis.