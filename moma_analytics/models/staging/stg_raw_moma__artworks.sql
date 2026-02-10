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
    "Acquisition Date"
  from {{ source('raw_moma', 'artworks') }}
),

cleaned as (
  select
    ObjectID::int as artwork_id,
    trim(Title) as artwork_title,
    -- Parse artist_id from "(12343)" format
    nullif(regexp_replace(ConstituentID, '[^0-9]', ''), '')::int as artist_id,
    Date as date_raw,
    Medium,
    Dimensions,
    "Acquisition Date"::date as acquisition_date
  from source_artworks
)

select
  artwork_id,
  artwork_title,
  artist_id,
  date_raw,
  Medium,
  Dimensions,
  acquisition_date
from cleaned
where artwork_id is not null

-- Description: Cleans artworks data. Trims titles, parses artist_id from parentheses format, casts dates. Filters null IDs.