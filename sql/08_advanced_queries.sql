-- ============================================================================
-- SQL Module: 08_advanced_queries.sql
-- Purpose: CTEs, recursive queries, database views, index design, and performance optimizations.
-- ============================================================================

-- BUSINESS QUESTION:
-- Create a recursive query that generates a sequential series of dates for a calendar, 
-- and joins it with daily sales. This identifies dates with zero platform sales (activity gaps).

-- QUERY:
WITH RECURSIVE CalendarDays AS (
    SELECT CAST('2017-01-01' AS DATE) AS day_date
    UNION ALL
    SELECT CAST(day_date + INTERVAL '1 day' AS DATE)
    FROM CalendarDays
    WHERE day_date < '2017-01-15' -- Limits recursion depth for sample execution
),
DailyRevenue AS (
    SELECT 
        CAST(order_purchase_timestamp AS DATE) AS purchase_date,
        SUM(payment_value) AS revenue
    FROM olist_orders_dataset o
    JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    GROUP BY 1
)
SELECT 
    c.day_date AS calendar_date,
    COALESCE(ROUND(d.revenue, 2), 0.0) AS daily_sales
FROM CalendarDays c
LEFT JOIN DailyRevenue d ON c.day_date = d.purchase_date
ORDER BY c.day_date;

-- EXPECTED BUSINESS INSIGHT:
-- Demonstrates the RECURSIVE CTE construct. By joining a calendar date series 
-- against sales, analysts can expose gaps or outages where daily transactions 
-- dropped to zero, signaling payment gateway failures or operational downtime.


-- ----------------------------------------------------------------------------
-- ADVANCED VIEW DESIGN:
-- Create a master order analytics view `vw_order_master` which pre-joins orders, 
-- customers, payment values, and average review ratings.

-- VIEW CREATION:
CREATE OR REPLACE VIEW vw_order_master AS 
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_state,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    -- Pay values sum
    COALESCE(p.payment_value_sum, 0.0) AS total_order_payment,
    -- Average reviews score
    COALESCE(r.avg_review_score, 0.0) AS average_review_score
FROM olist_orders_dataset o
LEFT JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
LEFT JOIN (
    SELECT order_id, SUM(payment_value) AS payment_value_sum
    FROM olist_order_payments_dataset
    GROUP BY order_id
) p ON o.order_id = p.order_id
LEFT JOIN (
    SELECT order_id, AVG(review_score) AS avg_review_score
    FROM olist_order_reviews_dataset
    GROUP BY order_id
) r ON o.order_id = r.order_id;


-- ----------------------------------------------------------------------------
-- INDEX RECOMMENDATIONS FOR DATABASE OPTIMIZATION:
-- In a database handling high-volume reads and joins, standard queries will slow 
-- down due to full table scans. We recommend implementing indexes on frequently 
-- joined foreign keys:

-- 1. Index on Orders table foreign key customer_id
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON olist_orders_dataset(customer_id);

-- 2. Index on Order Items table foreign keys
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON olist_order_items_dataset(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON olist_order_items_dataset(product_id);
CREATE INDEX IF NOT EXISTS idx_order_items_seller_id ON olist_order_items_dataset(seller_id);

-- 3. Index on Geolocation zip code prefix
CREATE INDEX IF NOT EXISTS idx_geolocation_zip ON olist_geolocation_dataset(geolocation_zip_code_prefix);


-- ----------------------------------------------------------------------------
-- DATABASE PERFORMANCE OPTIMIZATION TIPS:
-- 1. Query Execution Plans:
--    Always run `EXPLAIN ANALYZE <your_query>` before deploying to production. 
--    Look for "Seq Scan" (Sequential Scans) on large tables and verify if they can 
--    be replaced with "Index Scan".
-- 2. Table Partitioning:
--    For continental platforms, partition the `orders` and `order_items` tables 
--    by `order_purchase_timestamp` (yearly/monthly partitions) or by state 
--    boundaries to limit search ranges in geographic queries.
-- 3. Materialized Views:
--    If aggregating large monthly metrics for executive dashboards, replace standard 
--    views with `MATERIALIZED VIEW` and refresh them overnight using a cron job, 
--    reducing transactional database load during business hours.
