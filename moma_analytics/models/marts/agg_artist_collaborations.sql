{{
  config(
    materialized='table',
    tags=['analytics']
  )
}}

with fct as (
  select * from {{ ref('fct_artwork_acquisition') }}
),

artist_pairs as (
  select
    f1.artist_id as artist_1_id,
    f1.artist_name as artist_1_name,
    f2.artist_id as artist_2_id,
    f2.artist_name as artist_2_name,
    count(distinct case when f1.Medium = f2.Medium then f1.artwork_id end) as shared_medium_count,
    count(distinct case when f1.artist_nationality = f2.artist_nationality then f1.artwork_id end) as same_nationality_count,
    count(distinct case when abs(f1.acquisition_year - f2.acquisition_year) <= 5 then f1.artwork_id end) as acquired_close_in_time
  from fct f1
  join fct f2 on f1.artist_id < f2.artist_id
  group by f1.artist_id, f1.artist_name, f2.artist_id, f2.artist_name
  having count(*) > 0
)

select
  artist_1_name,
  artist_2_name,
  shared_medium_count,
  same_nationality_count,
  acquired_close_in_time,
  (shared_medium_count + same_nationality_count + acquired_close_in_time) as connection_score
from artist_pairs
order by connection_score desc

-- Description: Artist collaboration networks. Shows connections between artists (shared medium, nationality, acquisition timing).