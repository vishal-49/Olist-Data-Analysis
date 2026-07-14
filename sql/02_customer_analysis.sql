-- ============================================================================
-- SQL Module: 02_customer_analysis.sql
-- Purpose: Customer segment analysis, spending distributions, and repeat purchase checks.
-- ============================================================================

-- BUSINESS QUESTION:
-- Which customer states contribute the highest total revenue (GMV), number of orders, 
-- and average order value (AOV)?

-- QUERY:
SELECT 
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(p.payment_value) AS total_revenue,
    ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC;

-- EXPECTED BUSINESS INSIGHT:
-- Sao Paulo (SP), Rio de Janeiro (RJ), and Minas Gerais (MG) are top revenue drivers. 
-- Interestingly, although SP has the highest orders, some smaller remote states may 
-- have higher AOV due to increased freight costs.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- How often do customers place repeat orders? Calculate the distribution of 
-- order counts per customer_unique_id to evaluate loyalty.

-- QUERY:
WITH CustomerOrderCounts AS (
    SELECT 
        customer_unique_id,
        COUNT(order_id) AS total_orders
    FROM olist_orders_dataset o
    JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
    GROUP BY customer_unique_id
)
SELECT 
    total_orders AS orders_placed,
    COUNT(customer_unique_id) AS customer_count,
    ROUND(COUNT(customer_unique_id) * 100.0 / SUM(COUNT(customer_unique_id)) OVER(), 2) AS percentage_of_customers
FROM CustomerOrderCounts
GROUP BY total_orders
ORDER BY orders_placed;

-- EXPECTED BUSINESS INSIGHT:
-- Quantifies Olist's retention struggle. Over 96% of customer profiles have placed only 
-- a single order. The marketing team should trigger post-purchase incentives to boost repeat rates.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- List all combinations of customer states and seller states where transactions occurred. 
-- Include combinations with zero transactions to help expand seller networks.

-- QUERY:
WITH ActivePairs AS (
    SELECT DISTINCT 
        c.customer_state,
        s.seller_state
    FROM olist_orders_dataset o
    JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
    JOIN olist_order_items_dataset i ON o.order_id = i.order_id
    JOIN olist_sellers_dataset s ON i.seller_id = s.seller_id
)
SELECT 
    all_states.customer_state,
    all_states.seller_state,
    CASE WHEN ap.seller_state IS NOT NULL THEN 'Active Corridor' ELSE 'Inactive' END AS corridor_status
FROM (
    SELECT DISTINCT c1.customer_state, s1.seller_state 
    FROM olist_customers_dataset c1
    CROSS JOIN olist_sellers_dataset s1
) all_states
LEFT JOIN ActivePairs ap 
    ON all_states.customer_state = ap.customer_state 
   AND all_states.seller_state = ap.seller_state
ORDER BY corridor_status, all_states.customer_state;

-- EXPECTED BUSINESS INSIGHT:
-- Demonstrates the CROSS JOIN construct. This helps operations map geographic paths 
-- that currently lack transactions, highlighting where to target regional seller recruitment.
