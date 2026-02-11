{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

exhibition_stats as (
  select
    artist_nationality,
    Medium,
    count(distinct artwork_id) as artworks_in_exhibitions,
    count(distinct artist_id) as artists,
    round(avg(artist_age_at_acquisition), 1) as avg_artist_age,
    min(acquisition_year) as earliest_exhibition,
    max(acquisition_year) as latest_exhibition
  from fct
  where acquisition_year is not null
  group by artist_nationality, Medium
)

select
  artist_nationality,
  Medium,
  artworks_in_exhibitions,
  artists,
  avg_artist_age,
  earliest_exhibition,
  latest_exhibition,
  (latest_exhibition - earliest_exhibition) as exhibition_span_years
from exhibition_stats
order by artworks_in_exhibitions desc

-- Description: Exhibition analysis by nationality and medium. Shows exhibition history and artist representation.