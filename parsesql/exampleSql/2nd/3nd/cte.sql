
CREATE OR REPLACE VIEW myview COMMENT='Test asds' AS
WITH cte_sales_amounts AS (
    SELECT    
        first_name + ' ' + last_name, 
        SUM(quantity * list_price * (1 - discount)),
        YEAR(order_date)
    FROM    
        sales.orders o
    INNER JOIN sales.order_items i ON i.order_id = o.order_id
    INNER JOIN sales.staffs s ON s.staff_id = o.staff_id
    GROUP BY 
        first_name + ' ' + last_name,
        year(order_date)
)
, sub AS (
        SELECT    
        first_name + ' ' + last_name, 
        SUM(quantity * list_price * (1 - discount)),
        YEAR(order_date)
    FROM A
)
SELECT
    staff, 
    sales
FROM 
    cte_sales_amounts
WHERE
    year = 2018;