-- In this example, we use two WITH clauses, the second of which refers 
-- to the first.
with
   album_IDs_1976 as (select album_ID from music_albums where album_year = 1976),
   Journey_album_IDs as (select m.album_year, m.album_name, m.album_id, b.band_name from music_albums as m inner join music_bands as b where m.band_id = b.band_id and b.band_name = 'Journey')
select album_name, band_name from album_IDs_1976 inner join Journey_album_IDs where album_IDs_1976.album_id = Journey_album_IDs.album_ID
