-- 1. Total revenue by region
SELECT region, ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

-- 2. Monthly revenue trend
SELECT substr(order_date, 1, 7) AS month,
       ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY month
ORDER BY month;

-- 3. Top five products by revenue
SELECT product, ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC
LIMIT 5;

-- 4. Orders by region
SELECT region, COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY region
ORDER BY order_count DESC;
