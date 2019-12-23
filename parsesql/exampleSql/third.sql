    SELECT DATEADD(day,-1,pxd_upd_date),
    pbd_prod_code,
    psd_stk_qty+psd_booked_qty, 
    IFNULL(CONCAT(CONCAT(TRIM(TRAILING ' ' FROM P.pbd_prod_name),
    CASE LENGTH(CONVERT(VARCHAR(6), P.pbd_prod_ptr))
    WHEN '5' THEN
    CASE
    WHEN CONVERT(SQL_INTEGER,SUBSTRING(CONVERT(VARCHAR(6),P.pbd_prod_ptr),3)) <= 700
    THEN
    (SELECT TRIM(TRAILING ' ' FROM A.aca_cu_name)
    FROM admin.sffaca_details A
    WHERE A.aca_cu_no=CONCAT('PTX0', SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),1,2))
    AND A.aca_addr_no=CONVERT(SQL_INTEGER,SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),3)))
    ELSE
    (SELECT TRIM(TRAILING ' ' FROM aca_txt_l1)
    FROM admin.sffaca_other C
    WHERE C.aca_cu_no=CONCAT('PTX0', SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),1,2))
    AND C.aca_addr_no=CONVERT(SQL_INTEGER,SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),3)))
    END
    WHEN '6' THEN
    CASE
    WHEN CONVERT(SQL_INTEGER,SUBSTRING(CONVERT(VARCHAR(6),P.pbd_prod_ptr),4)) <= 700
    THEN
    (SELECT TRIM(TRAILING ' ' FROM A.aca_cu_name)
    FROM admin.sffaca_details A
    WHERE A.aca_cu_no=CONCAT('PTX', SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),1,3))
    AND A.aca_addr_no=CONVERT(SQL_INTEGER,SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),4)))
    ELSE
    (SELECT TRIM(TRAILING ' ' FROM aca_txt_l1)
    FROM admin.sffaca_other C
    WHERE C.aca_cu_no=CONCAT('PTX', SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),1,3))
    AND C.aca_addr_no=CONVERT(SQL_INTEGER,SUBSTRING(CONVERT(VARCHAR(6), P.pbd_prod_ptr),4)))
    END
    END),
    CONCAT(' ', CASE P.pbd_prod_unit WHEN 'Single' THEN '' ELSE P.pbd_prod_unit END)),
    CONCAT(TRIM(TRAILING ' ' FROM P.pbd_prod_name),
    CONCAT(' ', CASE P.pbd_prod_unit WHEN 'Single' THEN '' ELSE P.pbd_prod_unit END))) AS Description,
    (SELECT TOP 1 DATEADD(day,-1, A.bsj_putaway_date)
    FROM admin.sffbsj A
    WHERE A.bsj_prod_ptr=P.pbd_prod_ptr
    AND A.bsj_type=1
    ORDER BY A.bsj_move_date DESC, A.bsj_move_time DESC),
    pbd_prod_pack,
    pbd_vat_code,
    pbd_split_price,
    pbd_trade_price,
    pbd_retail_price,
    pbd_layer_qty,
    pbd_pallet_size,
    pxd_ean_code,
    pbd_maj_grp,
    pbd_min_grp,
    pxd_flags_1,
    pxd_flags_2,
    pbd_prod_ptr,
    CASE pbd_prod_unit WHEN 'Single' THEN '' ELSE pbd_prod_unit END,
    psd_po_qty from admin.sffpbd P
    LEFT JOIN admin.sffpsd S
    ON P.pbd_prod_ptr=S.psd_prod_ptr
    LEFT JOIN admin.sffpxd_details D
    ON P.pbd_prod_ptr=D.pxd_prod_ptr
    WHERE psd_stk_qty+psd_booked_qty+psd_po_qty>0
    ORDER BY pbd_maj_grp ASC,
    pbd_min_grp ASC,
    pbd_prod_name ASC