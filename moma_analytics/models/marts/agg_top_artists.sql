{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

artist_stats as (
  select
    artist_id,
    artist_name,
    artist_nationality,
    count(*) as artwork_count,
    count(distinct Medium) as medium_types,
    min(acquisition_year) as first_acquired,
    max(acquisition_year) as last_acquired
  from fct
  group by artist_id, artist_name, artist_nationality
)

select
  artist_id,
  artist_name,
  artist_nationality,
  artwork_count,
  medium_types,
  first_acquired,
  last_acquired,
  (last_acquired - first_acquired) as years_span
from artist_stats
order by artwork_count desc

-- Description: Top artists by number of works in collection. Shows artist productivity and diversity.