{{
  config(
    materialized='view',
    tags=['staging']
  )
}}

with source_artworks as (
  select
    ObjectID,
    Title,
    ConstituentID,
    Date,
    Medium,
    Dimensions,
    DateAcquired,
    "Height (cm)",
    "Width (cm)"
  from {{ source('raw_moma', 'artworks') }}
),

cleaned as (
  select
    try_cast(ObjectID as int) as artwork_id,
    trim(Title) as artwork_title,
    try_cast(regexp_replace(ConstituentID, '[^0-9]', '') as int) as artist_id,
    Date as date_raw,
    Medium,
    Dimensions,
    try_cast(DateAcquired as date) as acquisition_date,
    try_cast("Height (cm)" as float) as height_cm,
    try_cast("Width (cm)" as float) as width_cm
  from source_artworks
)

select
  artwork_id,
  artwork_title,
  artist_id,
  date_raw,
  Medium,
  Dimensions,
  acquisition_date,
  height_cm,
  width_cm
from cleaned
where artwork_id is not null and artist_id is not null

-- Description: Cleans artworks data. Handles invalid dates/dimensions with try_cast. Filters nulls.