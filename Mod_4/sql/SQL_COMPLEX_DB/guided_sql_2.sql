-- Talk about difference between WHERE and HAVING

SELECT
    product_id,
    product_name
FROM
    production.products
WHERE 
	product_name LIKE 'Surly%'
;

SELECT
    COUNT(product_id),
    product_name
FROM
    production.products
WHERE 
	product_name LIKE 'Surly%'
GROUP BY
	product_name
ORDER BY
	COUNT(product_id) DESC
;

-- Interesting, there are 2 Surly bikes with 2 different product_ids
-- If we wanted to filter by the COUNT, an aggregate function, we need to put filter 
-- the having clause
SELECT
    COUNT(product_id) AS cnt_id,
    product_name
FROM
    production.products
WHERE 
	product_name LIKE 'Surly%'
GROUP BY
	product_name
HAVING
    COUNT(product_id) = 2
ORDER BY
	COUNT(product_id) DESC
;

-- This example uses the COUNT() function with the GROUP BY 
-- clause to return the number orders for each order’s status:
SELECT    
    order_status, 
    COUNT(order_id) order_count
FROM    
    sales.orders
WHERE 
    YEAR(order_date) = 2018
GROUP BY 
    order_status
;

-- The values in the order_status column are numbers, 
-- which is not meaningful in this case. To make the output more understandable, 
-- you can use the simple CASE expression as shown in the following query:

SELECT    
    CASE order_status
        WHEN 1 THEN 'Pending'
        WHEN 2 THEN 'Processing'
        WHEN 3 THEN 'Rejected'
        WHEN 4 THEN 'Completed'
    END AS order_status, 
    COUNT(order_id) order_count
FROM    
    sales.orders
WHERE 
    YEAR(order_date) = 2018
GROUP BY 
    order_status
;

-- An example of using the CASE WHEN expression in aggregate function. In this way,
-- CASE WHEN statements can be used to aggregate and pivot our results.
SELECT    
    SUM(CASE
            WHEN order_status = 1
            THEN 1
            ELSE 0
        END) AS 'Pending', 
    SUM(CASE
            WHEN order_status = 2
            THEN 1
            ELSE 0
        END) AS 'Processing', 
    SUM(CASE
            WHEN order_status = 3
            THEN 1
            ELSE 0
        END) AS 'Rejected', 
    SUM(CASE
            WHEN order_status = 4
            THEN 1
            ELSE 0
        END) AS 'Completed', 
    COUNT(*) AS Total
FROM    
    sales.orders
WHERE 
    YEAR(order_date) = 2018
;

-- The following statement uses the searched CASE expression to 
-- classify sales order by order value:

SELECT    
    o.order_id, 
    SUM(quantity * list_price) order_value,
    CASE
        WHEN SUM(quantity * list_price) <= 500 
            THEN 'Very Low'
        WHEN SUM(quantity * list_price) > 500 AND 
            SUM(quantity * list_price) <= 1000 
            THEN 'Low'
        WHEN SUM(quantity * list_price) > 1000 AND 
            SUM(quantity * list_price) <= 5000 
            THEN 'Medium'
        WHEN SUM(quantity * list_price) > 5000 AND 
            SUM(quantity * list_price) <= 10000 
            THEN 'High'
        WHEN SUM(quantity * list_price) > 10000 
            THEN 'Very High'
    END order_priority
FROM    
    sales.orders o
INNER JOIN sales.order_items i ON i.order_id = o.order_id
WHERE 
    YEAR(order_date) = 2018
GROUP BY 
    o.order_id
;

-- without union all
SELECT 
  product_id, 
  product_name,
  list_price
FROM
  production.products
WHERE
  list_price > 100
OR
  list_price < 300
;

-- Using Union All, same as concat, axis = 0
(
SELECT 
  product_id, 
  product_name,
  list_price
FROM
  production.products
WHERE
  list_price > 100
) 
UNION ALL
-- UNION keyword does the same thing but only returns unique rows.
(
SELECT 
  product_id, 
  product_name,
  list_price
FROM
  production.products
WHERE
  list_price < 300
) 
;

-- WITH AS example

WITH a AS (
SELECT 
  product_id, 
  product_name,
  list_price
FROM
  production.products
WHERE
  list_price > 100
), b AS
(
SELECT 
  product_id, 
  product_name,
  list_price
FROM
  production.products
WHERE
  list_price < 300
) 

SELECT * FROM a
UNION ALL
SELECT * FROM b
;

-- Some subquery examples. 
-- SQL supports 32 levels of nesting!

SELECT
    product_name,
    list_price
FROM
    production.products
WHERE
    list_price > (
        SELECT
            AVG (list_price)
        FROM
            production.products
        WHERE
            brand_id IN (
                SELECT
                    brand_id
                FROM
                    production.brands
                WHERE
                    brand_name = 'Strider'
                OR brand_name = 'Trek'
            )
    )
ORDER BY
    list_price
;

-- Window functions
-- The following statement uses the ROW_NUMBER() to assign each customer row a sequential number:

SELECT 
   ROW_NUMBER() OVER (ORDER BY first_name) AS row_num,
   first_name, 
   last_name, 
   city
FROM 
   sales.customers
;

-- The following example uses the ROW_NUMBER() function to assign a sequential integer 
-- to each customer. It resets the number when the city changes:

SELECT 
   first_name, 
   last_name, 
   city,
   ROW_NUMBER() OVER (PARTITION BY city ORDER BY first_name) AS row_num
FROM 
   sales.customers
-- Try adding a where clause where row_num > 3
ORDER BY 
   city
;

-- Then show that a WITH AS will allow it to work:

WITH a AS (SELECT 
   first_name, 
   last_name, 
   city,
   ROW_NUMBER() OVER (PARTITION BY city ORDER BY first_name) AS row_num
FROM 
   sales.customers
ORDER BY 
   city)

SELECT * FROM a WHERE row_num > 3
;

-- Another way to handle it is to put it in the FROM clause as a subquery
SELECT
  *
FROM
    (SELECT 
	   first_name, 
	   last_name, 
	   city,
	   ROW_NUMBER() OVER (PARTITION BY city ORDER BY first_name) AS row_num
	FROM 
	   sales.customers
	ORDER BY 
	   city) a
WHERE
  a.row_num > 3
;

-- The following example uses the RANK() function to rank product by their list price:

SELECT
  product_id,
  product_name,
  list_price,
--  RANK() OVER (ORDER BY list_price DESC) price_rank 
--  first run without the rank function
FROM
  production.products
;


-- This example uses the RANK() function to assign a rank to each product by list price 
-- in each brand and returns products with rank less than or equal to three:

-- In the example below(explain after writing):

-- First, the PARTITION BY clause divides the products into partitions by brand Id.
-- Second, the ORDER BY clause sorts products in each partition by list prices.
-- Third, the outer query returns the products whose rank values are less than or equal to three.

-- The RANK() function is applied to each row in each partition and reinitialized 
-- when crossing the partition’s boundary.

SELECT * 
FROM (
    SELECT
        product_id,
        product_name,
        brand_id,
        list_price,
        RANK () OVER ( PARTITION BY brand_id ORDER BY list_price DESC
    ) price_rank 
 FROM
    production.products
) t
WHERE 
  price_rank <= 3
;

