-- SELECT the product_name and list price from the products table.

SELECT
  p.product_name,
  p.list_price
FROM
  production.products p 
;

-- 2 ways to grab distinct values in a column
-- first look at the data
SELECT
  p.model_year
FROM
  production.products p
;

-- DISTINCT keyword
SELECT
  DISTINCT p.model_year
FROM
  production.products p
;

-- Using Group By 
SELECT
  p.model_year
FROM
  production.products p
GROUP BY
  1
;

-- the product_name and list price from the products table where the product name begins with "Trek"
-- and the list price is less than or equal to 200 dollars.
SELECT
  p.product_name,
  p.list_price
FROM
  production.products p 
WHERE
  p.product_name LIKE 'Trek%'
AND
  p.list_price <= 200
;

-- Select the product names between $150 and $250 dollars
SELECT
  p.product_name,
  p.list_price
FROM
  production.products p 
WHERE
  p.list_price BETWEEN 150 AND 250
;

-- Perhaps we want to know out of our customers that are missing phone numbers, what are their email addresses?

SELECT
  c.first_name,
  c.last_name,
  c.email,
  c.phone
FROM
  sales.customers c
WHERE
  c.phone IS NULL
;

-- Example question: What is the distribution of email domains among  our most active and least active customers?

-- Return customers from New York City

SELECT
  *
FROM
  sales.customers c
WHERE
  c.city = 'New York'
;

-- Return how many orders where order status = rejected?
SELECT
  *
FROM
  sales.orders o
WHERE
  o.order_status = 3
;

-- From which stores were these rejections occurring in? Order by descending count
SELECT
  COUNT(*) AS cnt_rej,
  o.store_id AS store_id
FROM
  sales.orders o
WHERE
  o.order_status = 3
GROUP BY
  2
ORDER BY
  cnt_rej DESC
;



-- Let's analyze store 3 since it had the most order rejections. Find the staff contact information that work at that store.
SELECT 
  s.staff_id, 
  s.first_name, 
  s.last_name, 
  s.email, 
  s.phone
FROM 
  sales.staffs s 
WHERE 
  s.store_id = 3;
  
-- Merge the order details together with the staff information so you know which orders to ask about! 

SELECT 
  *
FROM 
  sales.staffs s
INNER JOIN
  sales.orders o
ON
  s.staff_id = o.staff_id
WHERE 
  s.store_id = 3;  
  
-- How many orders per staff? Look at not only store 3.
SELECT 
  s.staff_id,
  s.first_name,
  s.last_name,
  s.store_id,
  COUNT(o.order_status)
FROM 
  sales.staffs s
INNER JOIN
  sales.orders o
ON
  s.staff_id = o.staff_id
WHERE 
  s.store_id = 3
GROUP BY
  1, 2, 3 ;

-- Clearly some have way more orders than others. 
-- The store with the fewest overall orders happens to have the most order rejections.

SELECT 
  s.staff_id,
  s.first_name,
  s.last_name,
  s.store_id,
  COUNT(o.order_status) AS cnt_ord_stat
FROM 
  sales.staffs s
INNER JOIN
  sales.orders o
ON
  s.staff_id = o.staff_id
WHERE 
  s.store_id = 3
AND
  o.order_status = 3
GROUP BY
  1, 2, 3 
-- could also add here HAVING cnt_ord_stat > X
;

--------------------------
-- IN keyword

SELECT
    order_id,
    order_date,
    customer_id
FROM
    sales.orders
WHERE
    customer_id IN (50,51,52,59,68,26)
ORDER BY
    order_date DESC
;

-- IN operator with subquery
--  

SELECT
    order_id,
    order_date,
    customer_id
FROM
    sales.orders
WHERE
    customer_id IN (
        SELECT
            customer_id
        FROM
            sales.customers
        WHERE
            city = 'New York'
    )
ORDER BY
    order_date DESC
;


SELECT
    order_id,
    order_date,
    customer_id
FROM
    ( SELECT * FROM orders ) o
ORDER BY
    order_date DESC
;


