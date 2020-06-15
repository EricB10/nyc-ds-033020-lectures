1. Return the average list price for each brand.

SELECT
--   p.product_id,
--   p.product_name,
--   b.brand_id,
  b.brand_name,
  AVG(p.list_price)
FROM
  production.products p 
INNER JOIN
  production.brands b
ON
  p.brand_id = b.brand_id
GROUP BY
  1
;

2. Return the product_name, the brand_name, list price, and assign row numbers 
to each product (restarting with each brand) by list_price descending.

SELECT
   p.product_name,
   b.brand_name,
   p.list_price,
   ROW_NUMBER() OVER (PARTITION BY b.brand_name ORDER BY p.list_price DESC)
FROM
  production.products p 
INNER JOIN
  production.brands b
ON
  p.brand_id = b.brand_id
;

3. Return the highest priced item for each brand (do not worry if more than one item is the most expensive). 
-- Use one of the strategies we went over earlier.
SELECT * FROM
(SELECT
   p.product_name,
   b.brand_name,
   p.list_price,
   ROW_NUMBER() OVER (PARTITION BY b.brand_name ORDER BY p.list_price DESC) price_row
FROM
  production.products p 
INNER JOIN
  production.brands b
ON
  p.brand_id = b.brand_id
) a
WHERE
  a.price_row = 1
;