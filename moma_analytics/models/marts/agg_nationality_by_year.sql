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
  acquisition_year,
  artist_nationality,
  count(*) as artwork_count,
  count(distinct artist_id) as artist_count
from fct
where acquisition_year is not null and artist_nationality is not null
group by acquisition_year, artist_nationality
order by acquisition_year desc, artwork_count desc

-- Description: Artist nationality trends over time. Shows geographic diversity of acquisitions.