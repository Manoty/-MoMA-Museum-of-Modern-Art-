{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
)

select
  Medium,
  count(*) as artwork_count,
  count(distinct artist_id) as artist_count,
  round(avg(artist_age_at_acquisition), 1) as avg_artist_age,
  min(acquisition_year) as first_acquired,
  max(acquisition_year) as last_acquired
from fct
where Medium is not null
group by Medium
order by artwork_count desc

-- Description: Analytics mart aggregating artworks by medium/technique. Shows popularity and trends.