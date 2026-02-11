{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

with_decade as (
  select
    (acquisition_year / 10 * 10) as decade,
    Medium,
    artist_nationality,
    artwork_id,
    artist_id
  from fct
  where acquisition_year is not null
)

select
  decade,
  count(*) as artwork_count,
  count(distinct artist_id) as artist_count,
  count(distinct Medium) as medium_types,
  count(distinct artist_nationality) as nationality_count
from with_decade
group by decade
order by decade desc

-- Description: Acquisitions aggregated by decade. Shows collection growth trends over time.