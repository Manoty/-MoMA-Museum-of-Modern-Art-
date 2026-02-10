{{
  config(
    materialized='table',
    tags=['marts']
  )
}}

with artworks as (
  select * from {{ ref('stg_raw_moma__artworks') }}
),

artists as (
  select * from {{ ref('stg_raw_moma__artists') }}
),

joined as (
  select
    a.artwork_id,
    a.artist_id,
    ar.artist_name,
    ar.Nationality as artist_nationality,
    a.artwork_title,
    a.Medium,
    a.acquisition_date,
    extract(year from a.acquisition_date) as acquisition_year,
    extract(month from a.acquisition_date) as acquisition_month,
    extract(year from a.acquisition_date) - ar.birth_year as artist_age_at_acquisition,
    current_timestamp as dbt_loaded_at
  from artworks a
  left join artists ar on a.artist_id = ar.artist_id
  where a.acquisition_date is not null
)

select * from joined

-- Description: Fact table linking artworks to artists with acquisition context.