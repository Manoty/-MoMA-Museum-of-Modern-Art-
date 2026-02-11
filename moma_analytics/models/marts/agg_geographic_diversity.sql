{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with dim_artist as (
  select * from {{ ref('stg_raw_moma__artists') }}
),

fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

joined as (
  select
    ar.Nationality,
    count(distinct f.artwork_id) as total_artworks,
    count(distinct f.artist_id) as unique_artists,
    round(count(distinct f.artwork_id)::float / 
      (select count(*) from fct)::float * 100, 2) as pct_of_collection
  from fct f
  left join dim_artist ar on f.artist_id = ar.artist_id
  where ar.Nationality is not null
  group by ar.Nationality
)

select
  Nationality,
  total_artworks,
  unique_artists,
  pct_of_collection,
  row_number() over (order by total_artworks desc) as rank
from joined
order by total_artworks desc

-- Description: Geographic diversity. Shows which countries contribute most to collection.