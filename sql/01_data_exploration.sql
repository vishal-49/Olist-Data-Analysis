-- ============================================================================
-- SQL Module: 01_data_exploration.sql
-- Purpose: Initial data profiling, record counts, null checks, and basic joins.
-- ============================================================================

-- BUSINESS QUESTION:
-- What is the total size of our operational footprint (total orders, unique customers, 
-- unique products, and unique sellers active on the platform)?

-- QUERY:
SELECT 
    (SELECT COUNT(*) FROM olist_orders_dataset) AS total_orders,
    (SELECT COUNT(DISTINCT customer_unique_id) FROM olist_customers_dataset) AS unique_customers,
    (SELECT COUNT(DISTINCT product_id) FROM olist_products_dataset) AS unique_products,
    (SELECT COUNT(*) FROM olist_sellers_dataset) AS total_sellers;

-- EXPECTED BUSINESS INSIGHT:
-- Quantifies the overall size of Olist. We see a high customer count (~96k) 
-- relative to sellers (~3k), indicating a typical high-demand consumer marketplace.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- How are orders distributed across various order statuses? Do we have a high 
-- rate of cancellations or incomplete orders?

-- QUERY:
SELECT 
    order_status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS order_percentage
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY order_count DESC;

-- EXPECTED BUSINESS INSIGHT:
-- Over 97% of orders are in 'delivered' state. Canceled orders represent less than 1%, 
-- but identifying what triggers cancellations (e.g., shipping lag) is crucial for retention.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- Do we have review titles or commentary with missing entries? Standardize text values 
-- by replacing null review descriptions and titles.

-- QUERY:
SELECT 
    review_id,
    order_id,
    review_score,
    COALESCE(review_comment_title, 'no_title') AS sanitized_title,
    COALESCE(review_comment_message, 'no_message') AS sanitized_message
FROM olist_order_reviews_dataset
WHERE review_comment_message IS NULL
LIMIT 5;

-- EXPECTED BUSINESS INSIGHT:
-- Demonstrates standard data cleaning using COALESCE in SQL. Fills null values to 
-- prepare text fields for indexing or downstream sentiment analysis.
