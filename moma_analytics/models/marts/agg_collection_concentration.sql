{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

artist_counts as (
  select
    artist_id,
    artist_name,
    artist_nationality,
    count(*) as artwork_count
  from fct
  group by artist_id, artist_name, artist_nationality
),

ranked as (
  select
    artist_id,
    artist_name,
    artist_nationality,
    artwork_count,
    row_number() over (order by artwork_count desc) as rank,
    sum(artwork_count) over (order by artwork_count desc) as cumulative_artworks,
    (select count(*) from fct) as total_collection_size,
    round(sum(artwork_count) over (order by artwork_count desc)::float / 
          (select count(*) from fct)::float * 100, 2) as cumulative_pct
  from artist_counts
)

select
  rank,
  artist_name,
  artist_nationality,
  artwork_count,
  cumulative_artworks,
  total_collection_size,
  cumulative_pct
from ranked
where rank <= 100

-- Description: Collection concentration. Shows how many top artists represent X% of the collection (Pareto analysis).