-- ============================================================================
-- SQL Module: 04_product_analysis.sql
-- Purpose: Product category analysis, sales contribution, and ABC classification.
-- ============================================================================

-- BUSINESS QUESTION:
-- Apply ABC classification to product categories. Categorize them into:
-- Class A (top 80% of cumulative revenue), Class B (next 15%), Class C (bottom 5%).

-- QUERY:
WITH CategoryRevenue AS (
    SELECT 
        COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
        SUM(i.price) AS total_revenue
    FROM olist_order_items_dataset i
    JOIN olist_products_dataset p ON i.product_id = p.product_id
    LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
    GROUP BY 1
),
CategoryCumulative AS (
    SELECT 
        category,
        total_revenue,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) AS cumulative_revenue,
        SUM(total_revenue) OVER () AS total_platform_revenue
    FROM CategoryRevenue
),
CategoryPercentages AS (
    SELECT 
        category,
        total_revenue,
        ROUND(total_revenue * 100.0 / total_platform_revenue, 2) AS rev_pct,
        ROUND(cumulative_revenue * 100.0 / total_platform_revenue, 2) AS cum_rev_pct
    FROM CategoryCumulative
)
SELECT 
    category,
    total_revenue,
    rev_pct,
    cum_rev_pct,
    CASE 
        WHEN cum_rev_pct <= 80.0 THEN 'Class A (Core)'
        WHEN cum_rev_pct <= 95.0 THEN 'Class B (Secondary)'
        ELSE 'Class C (Long-Tail)'
    END AS abc_class
FROM CategoryPercentages
ORDER BY total_revenue DESC;

-- EXPECTED BUSINESS INSIGHT:
-- Segments catalog performance in SQL. Class A items (like health_beauty, watches_gifts) 
-- should receive optimal logistics flow and premium placement on partner sites.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- Identify the top 3 best-selling products (by total revenue) within each category.

-- QUERY:
WITH ProductRevenue AS (
    SELECT 
        COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
        i.product_id,
        SUM(i.price) AS product_sales,
        COUNT(i.order_id) AS items_sold
    FROM olist_order_items_dataset i
    JOIN olist_products_dataset p ON i.product_id = p.product_id
    LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
    GROUP BY 1, 2
),
RankedProducts AS (
    SELECT 
        category,
        product_id,
        product_sales,
        items_sold,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY product_sales DESC) AS sales_rank
    FROM ProductRevenue
)
SELECT 
    category,
    product_id,
    product_sales,
    items_sold,
    sales_rank
FROM RankedProducts
WHERE sales_rank <= 3
ORDER BY category, sales_rank;

-- EXPECTED BUSINESS INSIGHT:
-- Pinpoints specific top listings (SKUs) within categories. This is extremely useful for 
-- promotional bundling and allocating advertising spend to high-converting listings.
