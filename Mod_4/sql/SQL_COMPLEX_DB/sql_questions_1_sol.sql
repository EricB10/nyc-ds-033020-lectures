-- 1
SELECT
    city,
    COUNT(*)
FROM
    sales.customers
WHERE
    state = 'CA'
GROUP BY
    city
ORDER BY
    city
;

-- 2
SELECT
    city,
    COUNT(*)
FROM
    sales.customers
WHERE
    state = 'CA'
GROUP BY
    city
HAVING
    COUNT(*) > 10
ORDER BY
    city
;

-- 3
SELECT
    city,
    state,
    zip_code
FROM
    sales.customers
GROUP BY
    city, 
    state, 
    zip_code
-- ORDER BY
--     city, 
--     state, 
--     zip_code
;

-- 4
SELECT DISTINCT
   	city,
   	state,
   	zip_code
FROM
    sales.customers
;

-- 5
SELECT
    product_id,
    product_name,
    category_id,
    model_year,
    list_price
FROM
    production.products
WHERE
    list_price > 3000 OR model_year = 2018
ORDER BY
    list_price DESC
;

-- 6
SELECT
    product_id,
    product_name,
    category_id,
    model_year,
    list_price
FROM
    production.products
WHERE
    list_price BETWEEN 1899.00 AND 1999.99
ORDER BY
    list_price DESC
;

-- 7
SELECT
    product_id,
    product_name,
    category_id,
    model_year,
    list_price
FROM
    production.products
WHERE
    list_price IN (299.99, 369.99, 489.99)
ORDER BY
    list_price DESC
;

-- 8
SELECT
  AVG(p.list_price)
FROM
  production.products p 
WHERE
  p.product_name LIKE '%Cruiser%'
;

-- 9
SELECT
  c.customer_id,
  c.first_name,
  c.last_name,
  c.phone
FROM
  sales.customers c
WHERE
  c.phone IS NOT NULL
ORDER BY 
  c.last_name DESC
;

-- 10
SELECT 
  o.order_id,
  o.required_date
FROM 
  sales.orders o
WHERE 
  o.required_date BETWEEN CAST('2017-01-01' AS DATETIME) AND CAST('2017-01-31' AS DATETIME)
;

-- 11
SELECT
    o.order_id,
    o.order_status,
    SUM(oi.quantity * oi.list_price) AS total
FROM
    sales.orders o
INNER JOIN 
    sales.order_items oi
ON 
    o.order_id = oi.order_id
GROUP BY 
    order_id
;

-- 12
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

-- 13
SELECT
  c.first_name,
  c.last_name,
  c.email,
  c.phone,
  COUNT(o.order_id)
FROM
  sales.customers c
LEFT JOIN
  sales.orders o
ON
  c.customer_id = o.customer_id
WHERE
  c.phone IS NULL
GROUP BY
  1,2,3,4
;
