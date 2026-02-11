{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with dim_artwork as (
  select * from {{ ref('dim_artwork') }}
),

with_decade as (
  select
    (extract(year from acquisition_date) / 10 * 10) as decade,
    artwork_id,
    height_cm,
    width_cm,
    area_cm2
  from dim_artwork
  where acquisition_date is not null and area_cm2 is not null
)

select
  decade,
  count(*) as artwork_count,
  round(avg(height_cm), 2) as avg_height_cm,
  round(avg(width_cm), 2) as avg_width_cm,
  round(avg(area_cm2), 2) as avg_area_cm2,
  round(min(area_cm2), 2) as min_area_cm2,
  round(max(area_cm2), 2) as max_area_cm2
from with_decade
group by decade
order by decade desc

-- Description: Artwork size trends over time. Shows if newer artworks are larger/smaller.