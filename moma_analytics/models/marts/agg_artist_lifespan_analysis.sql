{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with dim_artist as (
  select * from {{ ref('dim_artist') }}
),

fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

joined as (
  select
    da.artist_id,
    da.artist_name,
    da.Nationality,
    da.birth_year,
    da.death_year,
    da.age_years,
    count(distinct f.artwork_id) as total_artworks,
    min(f.acquisition_year) as first_acquired,
    max(f.acquisition_year) as last_acquired,
    round(avg(f.acquisition_year - da.birth_year), 1) as avg_age_at_acquisition,
    (da.death_year - da.birth_year) as lifespan_years
  from dim_artist da
  left join fct f on da.artist_id = f.artist_id
  where da.birth_year is not null
  group by da.artist_id, da.artist_name, da.Nationality, da.birth_year, da.death_year, da.age_years
)

select
  artist_id,
  artist_name,
  Nationality,
  birth_year,
  death_year,
  age_years,
  lifespan_years,
  total_artworks,
  first_acquired,
  last_acquired,
  avg_age_at_acquisition
from joined
order by total_artworks desc

-- Description: Artist lifespan analysis. Shows relationship between artist age/lifespan and collection presence.