{{
  config(
    materialized='view',
    tags=['staging']
  )
}}

with source_artists as (
  select
    ConstituentID,
    DisplayName,
    Nationality,
    Gender,
    BeginDate,
    EndDate
  from {{ source('raw_moma', 'artists') }}
),

cleaned as (
  select
    ConstituentID::int as artist_id,
    DisplayName as artist_name,
    Nationality,
    Gender,
    -- Handle invalid dates gracefully
    try_cast(BeginDate as int) as birth_year,
    try_cast(EndDate as int) as death_year,
    row_number() over (partition by ConstituentID order by DisplayName) as rn
  from source_artists
)

select
  artist_id,
  artist_name,
  Nationality,
  Gender,
  birth_year,
  death_year
from cleaned
where rn = 1

-- Description: Deduplicated, cleaned artists from raw source. Handles invalid dates with try_cast.