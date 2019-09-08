with album_info_1976 as 
(
    select m.album_ID, m.album_name, b.band_name
      from music_albums as m inner join music_bands as b
      where m.band_id = b.band_id and album_year = 1976
)
SELECT ID, NAME, AGE, AMOUNT
   FROM CUSTOMERS, ORDERS, PRODUCT
   WHERE  CUSTOMERS.ID = ORDERS.CUSTOMER_ID;