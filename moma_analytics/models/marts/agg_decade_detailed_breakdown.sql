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
    artist_nationality,
    Medium,
    artwork_id,
    artist_id,
    acquisition_year
  from fct
  where acquisition_year is not null
)

select
  decade,
  artist_nationality,
  Medium,
  count(*) as artwork_count,
  count(distinct artist_id) as artist_count,
  round(count(*)::float / 
    (select count(*) from with_decade where decade = wd.decade)::float * 100, 2) as pct_of_decade
from with_decade wd
group by decade, artist_nationality, Medium
order by decade desc, artwork_count desc

-- Description: Detailed decade breakdown by nationality and medium. Shows collection composition per decade.