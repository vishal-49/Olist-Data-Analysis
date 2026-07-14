# Power BI Dashboard Page-by-Page Blueprint

This document details the layout, chart selection, filters, and interactivity guidelines for the 6-page executive-facing Power BI dashboard.

---

## Theme & Visual Standards

- **Theme Palette**: *Sleek Corporate Dark* or *Minimalist Professional Light*.
  - Primary Dark: `#1E2229` (Backgrounds)
  - Accent Color: `#00A896` (Teal - for revenue and core metrics)
  - Warning Color: `#F25F5C` (Soft Red - for late deliveries/negative reviews)
  - Neutral Dark: `#2D3142` (Card and chart containers)
  - Typography: **Segoe UI** or **Trebuchet MS** (for modern look)
- **KPI Card Design**: Large value numbers in top center with micro sparklines beneath showing monthly trends.
- **Interactivity**: Turn on **Cross-Filtering** across all charts on a page to enable deep slicing. Use **Drill Down** on hierarchies.

---

## Page 1: Executive Summary

*Goal: High-level health check of Olist platform for C-suite stakeholders.*

### Layout Blueprint

- **Top Row (KPI Cards)**:
  - `Total Revenue (GMV)` | `Total Orders` | `Total Customers` | `Total Sellers` | `Average Review Score` | `Late Delivery Rate`
- **Left Column (Filters & Navigation)**:
  - Year/Quarter/Month Slicers (Dropdowns).
  - Navigation button bar: links to Sales, Customer, Seller, Delivery, and Review dashboards.
- **Main Section (Charts)**:
  - **Chart 1 (Combo Chart)**: Monthly Revenue (Line) and Order Volumes (Column) over time. Include drill-down from Year -> Quarter -> Month.
  - **Chart 2 (Donut Chart)**: Revenue Share by ABC Category Class (Class A vs Class B vs Class C).
  - **Chart 3 (Horizontal Bar Chart)**: Top 5 States by Revenue (GMV).
- **Drill-through Action**: Right-clicking a state bar drill-through to the Geographic Analysis page.

---

## Page 2: Sales & Financial Analysis

*Goal: Investigate product categories and geographical distribution.*

### Layout Blueprint

- **Top KPI Cards**:
  - `Total Sales` | `Average Order Value (AOV)` | `Average Shipping cost (Freight)`
- **Filters**:
  - Customer State (Slicer), Category Class (Slicer).
- **Main Section (Charts)**:
  - **Chart 1 (Clustered Column Chart)**: Revenue vs. Freight Value by top 10 categories. Shows which categories are freight-heavy.
  - **Chart 2 (Treemap)**: Category GMV share, showing sizes of individual categories.
  - **Chart 3 (Map Visual)**: Bubble map of Brazil showing GMV size by zip code prefix/city (using lat/lng coordinate centroids).
  - **Chart 4 (Data Table)**: Top 20 products. Columns: `Product ID`, `Category`, `Price`, `Freight`, `Units Sold`, `Total GMV`.

---

## Page 3: Customer Dashboard

*Goal: Track customer acquisition, spending tiers, and repeat purchasing.*

### Layout Blueprint

- **Top KPI Cards**:
  - `Total Customers` | `Repeat Purchase Rate (RPR)` | `VIP Champion Count`
- **Filters**:
  - Customer Segment Slicer (VIP Champions, Loyal Mid-Tier, New High Spenders, One-Off Buyers).
- **Main Section (Charts)**:
  - **Chart 1 (Stacked Bar Chart)**: Customer segment counts showing composition of database.
  - **Chart 2 (Line Chart)**: Cumulative Customer Growth over time.
  - **Chart 3 (Scatter Plot)**: Recency (days) vs. Monetary (spend) for RFM groups to show cluster positions.
  - **Chart 4 (Matrix Visual)**: Customer spending distribution by state. Columns: `State`, `Active Customers`, `Total GMV`, `AOV`.

---

## Page 4: Seller Dashboard

*Goal: Monitor seller performance and identify high-risk accounts.*

### Layout Blueprint

- **Top KPI Cards**:
  - `Total Sellers` | `Average Seller Performance Score` | `Underperforming Sellers Count (Score < 50)`
- **Filters**:
  - Seller State Slicer, Seller Performance Rating Slicer.
- **Main Section (Charts)**:
  - **Chart 1 (Scatter Plot)**: Seller Total Sales (X-axis) vs. Average Review Score (Y-axis), sized by Order Count.
  - **Chart 2 (Bar Chart)**: Late Delivery Rate by top 10 sellers (with at least 20 items sold).
  - **Chart 3 (Matrix Visual)**: Underperforming sellers lookup. Columns: `Seller ID`, `Seller State`, `Total Orders`, `Sales Value`, `Late Rate`, `Rating`, `Performance Score`.
- **Tooltip Action**: Hovering over a Seller ID shows a tooltip card displaying their top 3 product categories and primary carrier delay.

---

## Page 5: Delivery & Logistics Dashboard

*Goal: Optimize shipping routes, carrier performance, and EDD SLA.*

### Layout Blueprint

- **Top KPI Cards**:
  - `Average Delivery Days` | `Late Delivery Rate (LDR)` | `Average Delay Days`
- **Filters**:
  - Shipping Corridor (Seller State to Customer State) Slicer.
- **Main Section (Charts)**:
  - **Chart 1 (Histogram/Bar Chart)**: Distribution of delivery lead times (bins: 1-5 days, 6-10 days, 11-15 days, 16+ days).
  - **Chart 2 (Horizontal Bar Chart)**: Late Delivery Rate by customer state.
  - **Chart 3 (Line Chart)**: Estimated vs. Actual Delivery Days Trend by month (to see if estimates are improving).
  - **Chart 4 (Matrix Visual)**: Carrier Performance Matrix. Columns: `Corridor (From/To)`, `Order Volume`, `Avg Transit Days`, `Avg Late Days`, `SLA Breach Rate`.

---

## Page 6: Review & NPS Dashboard

*Goal: Evaluate customer feedback loops and identify operational issues.*

### Layout Blueprint

- **Top KPI Cards**:
  - `Average Review Rating` | `Positive Review Share (%)` | `Negative Review Share (%)`
- **Filters**:
  - Review Score (1 to 5 Stars) Slicer.
- **Main Section (Charts)**:
  - **Chart 1 (Bar Chart)**: Star Rating Count (1-star to 5-star distribution).
  - **Chart 2 (Line Chart)**: Average Rating Trend over time.
  - **Chart 3 (Scatter Plot)**: Actual delivery delay (X-axis) vs. Average review rating (Y-axis).
  - **Chart 4 (Table Visual)**: Complaints log. Columns: `Order ID`, `Review Score`, `Delivery Delay`, `Sanitized Review Comment`. Include text search filter to locate keywords (e.g. "delay", "broken", "wrong product").
