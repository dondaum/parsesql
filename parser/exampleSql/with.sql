Create or replace view ae_aml.aml_v_product (album_name, COL_DIFF) AS
with album_info_1976 as 
(
    select m.album_ID, m.album_name, b.band_name
      from music_albums as m inner join music_bands as b
      where m.band_id = b.band_id and album_year = 1976
),
journey_album_info_1976 as 
(
    select *
      from album_info_1976 
      where band_name = 'Journey'
)
select album_name, band_name 
   from Journey_album_info_1976;