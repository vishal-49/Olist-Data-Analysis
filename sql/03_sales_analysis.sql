-- ============================================================================
-- SQL Module: 03_sales_analysis.sql
-- Purpose: Sales growth analysis, running totals, moving averages, and seasonality.
-- ============================================================================

-- BUSINESS QUESTION:
-- Calculate the monthly revenue (GMV) and a cumulative running total of revenue 
-- over time to show growth velocity to stakeholders.

-- QUERY:
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month,
        SUM(p.payment_value) AS monthly_revenue
    FROM olist_orders_dataset o
    JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
)
SELECT 
    TO_CHAR(order_month, 'YYYY-MM') AS month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY order_month), 2) AS running_total_revenue
FROM MonthlyRevenue
ORDER BY order_month;

-- EXPECTED BUSINESS INSIGHT:
-- Shows the cumulative billing curve. It demonstrates how fast the company accumulates 
-- cash flow, proving strong acquisition momentum.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- Calculate Month-over-Month (MoM) growth rates in revenue. Highlight periods 
-- of high seasonality.

-- QUERY:
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', CAST(order_purchase_timestamp AS TIMESTAMP)) AS order_month,
        SUM(payment_value) AS revenue
    FROM olist_orders_dataset o
    JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
),
LaggedRevenue AS (
    SELECT 
        order_month,
        revenue,
        LAG(revenue, 1) OVER (ORDER BY order_month) AS prior_month_revenue
    FROM MonthlyRevenue
)
SELECT 
    TO_CHAR(order_month, 'YYYY-MM') AS month,
    ROUND(revenue, 2) AS current_revenue,
    ROUND(prior_month_revenue, 2) AS prior_revenue,
    ROUND((revenue - prior_month_revenue) * 100.0 / prior_month_revenue, 2) AS mom_growth_pct
FROM LaggedRevenue
ORDER BY order_month;

-- EXPECTED BUSINESS INSIGHT:
-- Quantifies the MoM sales spikes. November 2017 shows an enormous spike (~60%+) 
-- due to Black Friday, whereas December/January show mild declines.


-- ----------------------------------------------------------------------------
-- BUSINESS QUESTION:
-- Compute a 3-month moving average of monthly revenue to smooth out seasonal noise.

-- QUERY:
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', CAST(order_purchase_timestamp AS TIMESTAMP)) AS order_month,
        SUM(payment_value) AS revenue
    FROM olist_orders_dataset o
    JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
)
SELECT 
    TO_CHAR(order_month, 'YYYY-MM') AS month,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(AVG(revenue) OVER (
        ORDER BY order_month 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS three_month_moving_avg
FROM MonthlyRevenue
ORDER BY order_month;

-- EXPECTED BUSINESS INSIGHT:
-- The 3-month moving average filters out short-term spikes (like Black Friday), 
-- presenting a clearer view of underlying platform growth for financial planning.
