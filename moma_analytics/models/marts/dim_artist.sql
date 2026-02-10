{{
  config(
    materialized='table',
    tags=['marts']
  )
}}

with stg_artists as (
  select * from {{ ref('stg_raw_moma__artists') }}
),

enriched as (
  select
    artist_id,
    artist_name,
    Nationality,
    Gender,
    birth_year,
    death_year,
    case when death_year is null then true else false end as is_living,
    case 
      when death_year is not null then death_year - birth_year
      else extract(year from current_date()) - birth_year
    end as age_years,
    current_timestamp as dbt_loaded_at
  from stg_artists
  where birth_year is not null
)

select * from enriched

-- Description: Dimension table for artists with calculated fields (is_living, age_years). One row per unique artist.