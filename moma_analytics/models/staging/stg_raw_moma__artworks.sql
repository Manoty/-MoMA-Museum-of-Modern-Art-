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
    ObjectID::int as artwork_id,
    trim(Title) as artwork_title,
    -- Parse artist_id from ConstituentID (may have multiple IDs)
    nullif(regexp_replace(ConstituentID, '[^0-9]', ''), '')::int as artist_id,
    Date as date_raw,
    Medium,
    Dimensions,
    DateAcquired::date as acquisition_date,
    "Height (cm)"::float as height_cm,
    "Width (cm)"::float as width_cm
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

-- Description: Cleans artworks data. Trims titles, parses artist_id, casts dates. Filters null IDs.