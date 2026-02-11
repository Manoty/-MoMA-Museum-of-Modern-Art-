-- Checking our tables n what we can analyze
SELECT 
  COUNT(*) as total_records,
  COUNT(DISTINCT artwork_id) as unique_artworks,
  COUNT(DISTINCT artist_id) as unique_artists,
  COUNT(DISTINCT acquisition_year) as years_span,
  COUNT(DISTINCT artist_nationality) as nationalities,
  COUNT(DISTINCT Medium) as mediums
FROM fct_artwork_acquisition;

SELECT DISTINCT Medium FROM fct_artwork_acquisition LIMIT 20;