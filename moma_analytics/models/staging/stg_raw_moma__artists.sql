{{
  config(
    materialized='view',
    tags=['staging']
  )
}}

with source_artists as (
  select
    ConstituentID,
    Name,
    Nationality,
    Gender,
    BeginDate,
    EndDate
  from {{ source('raw_moma', 'artists') }}
),

cleaned as (
  select
    ConstituentID::int as artist_id,
    Name as artist_name,
    Nationality,
    Gender,
    BeginDate::int as birth_year,
    case when EndDate = '' then null else EndDate::int end as death_year,
    row_number() over (partition by ConstituentID order by Name) as rn
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

-- Description: Deduplicated, cleaned artists from raw source. Removes duplicate ConstituentIDs, casts dates to integers.