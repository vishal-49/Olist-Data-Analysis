-- ============================================================================
-- SQL Module: 05_seller_analysis.sql
-- Purpose: Seller performance analysis, high-risk flags, and self-joins.
-- ============================================================================

-- BUSINESS QUESTION:
-- Identify high-volume, low-rated sellers. Find sellers who have fulfilled at least 
-- 50 order items and have an average review score below 3.0.

-- QUERY:
SELECT 
    i.seller_id,
    s.seller_state,
    s.seller_city,
    COUNT(i.order_item_id) AS total_items_sold,
    SUM(i.price) AS total_sales_value,
    ROUND(AVG(r.review_score), 2) AS average_review_score
FROM olist_order_items_dataset i
JOIN olist_sellers_dataset s ON i.seller_id = s.seller_id
JOIN olist_order_reviews_dataset r ON i.order_id = r.order_id
GROUP BY i.seller_id, s.seller_state, s.seller_city
HAVING COUNT(i.order_item_id) >= 50 AND AVG(r.review_score) < 3.0
ORDER BY average_review_score ASC;

-- EXPECTED BUSINESS INSIGHT:
-- Flags major liability accounts. Sellers who have high sales count but low ratings 
-- are highly damaging to customer retention. They should be prioritized for quality audits.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- Are there instances of different sellers listed under the same zip code prefix but 
-- located in different cities or states? (Self join on sellers).

-- QUERY:
SELECT DISTINCT
    s1.seller_zip_code_prefix,
    s1.seller_id AS seller_1_id,
    s1.seller_city AS seller_1_city,
    s1.seller_state AS seller_1_state,
    s2.seller_id AS seller_2_id,
    s2.seller_city AS seller_2_city,
    s2.seller_state AS seller_2_state
FROM olist_sellers_dataset s1
JOIN olist_sellers_dataset s2 
    ON s1.seller_zip_code_prefix = s2.seller_zip_code_prefix 
   AND s1.seller_id < s2.seller_id  -- Prevents mirror duplicates (A, B) and (B, A)
WHERE s1.seller_city <> s2.seller_city OR s1.seller_state <> s2.seller_state
ORDER BY s1.seller_zip_code_prefix
LIMIT 10;

-- EXPECTED BUSINESS INSIGHT:
-- Demonstrates self join. This query highlights inconsistencies in the registration 
-- geodata (for example, where sellers sharing a zip code prefix are categorized 
-- in different cities). Helps database administrators clean zip code tables.
