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
  Medium,
  count(*) as artwork_count,
  count(distinct artist_id) as artist_count
from fct
where acquisition_year is not null and Medium is not null
group by acquisition_year, Medium
order by acquisition_year desc, artwork_count desc

-- Description: Medium popularity over time. Shows which materials were acquired when.