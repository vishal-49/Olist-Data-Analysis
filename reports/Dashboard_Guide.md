# Power BI Dashboard Deployment & Usage Guide

This guide details how to build, model, and deploy the Olist Executive Dashboard using Power BI Desktop, utilizing the processed datasets and DAX formulas provided.

---

## 1. Importing Cleaned Data

Import the following processed CSV files from the `data/processed/` directory into Power BI Desktop:
1. `master_orders_dataset.csv`
2. `olist_customers_dataset.csv`
3. `olist_sellers_dataset.csv`
4. `olist_products_dataset.csv`

Ensure all date fields are recognized as `Date/Time` types (e.g. `order_purchase_timestamp`, `order_delivered_customer_date`).

---

## 2. Modeling Schema (Star Schema)

Navigate to the **Model View** and configure the relationships as shown below:

```
        +----------------------------+
        |        DimCustomers        |
        |  [customer_unique_id] (1)  |
        +-------------+--------------+
                      |
                      | (1:N)
                      v
+---------------------+---------------------+
|             FactOrders (Master)           |
|  [customer_unique_id]  | [order_purchase] |
+-------------+------------------+----------+
              | (N:1)            | (N:1)
              |                  |
              v                  v
        +-----+------+     +-----+------+
        |  DimSellers|     |   DimDate  |
        | [seller_id]|     |   [Date]   |
        +------------+     +------------+
```

### Relationship Properties
- **DimCustomers to FactOrders**:
  - Columns: `customer_unique_id`
  - Cardinality: One-to-many (1:*)
  - Cross filter direction: Single (DimCustomers filters FactOrders)
- **DimSellers to FactOrders**:
  - Columns: `seller_id`
  - Cardinality: One-to-many (1:*)
- **DimDate to FactOrders**:
  - Columns: `Date` to `order_purchase_timestamp` (Date part)
  - Cardinality: One-to-many (1:*)

---

## 3. Creating DAX Tables & Measures

### 3.1 Create Calendar Table
Go to **Modeling > New Table** and enter the DAX formula for `DimDate`:
```dax
DimDate = 
VAR MinDate = MIN(master_orders_dataset[order_purchase_timestamp])
VAR MaxDate = MAX(master_orders_dataset[order_purchase_timestamp])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "MonthNum", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "MonthYear", FORMAT([Date], "MMM YYYY"),
    "MonthYearSort", YEAR([Date]) * 100 + MONTH([Date]),
    "IsWeekend", IF(WEEKDAY([Date], 2) >= 6, "Weekend", "Weekday")
)
```
*Note: Select the `MonthYear` column, and set "Sort by Column" to `MonthYearSort`.*

### 3.2 Implement Core Measures
Click **New Measure** on `FactOrders` and implement:
- **Total Revenue**: `Total Revenue = SUM(master_orders_dataset[revenue_per_order])`
- **Total Orders**: `Total Orders = DISTINCTCOUNT(master_orders_dataset[order_id])`
- **AOV**: `Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)`
- **Late Delivery Rate**:
  ```dax
  Late Delivery Rate = 
  DIVIDE(
      CALCULATE([Total Orders], master_orders_dataset[late_delivery_flag] = 1),
      CALCULATE([Total Orders], NOT(ISBLANK(master_orders_dataset[order_delivered_customer_date]))),
      0
  )
  ```
- **Repeat Purchase Rate (RPR)**:
  ```dax
  Repeat Purchase Rate = 
  VAR MultiBuyers = 
      COUNTROWS(
          FILTER(
              VALUES(master_orders_dataset[customer_unique_id]),
              CALCULATE(DISTINCTCOUNT(master_orders_dataset[order_id])) > 1
          )
      )
  RETURN
      DIVIDE(MultiBuyers, DISTINCTCOUNT(master_orders_dataset[customer_unique_id]), 0)
  ```

---

## 4. Page-by-Page Layout Deployment

Build out the 6 pages described in `dashboard/dashboard_design_guide.md` using standard visuals:
- **Page 1 (Executive Summary)**: Focus on high-level KPI cards, the monthly revenue line chart, and the Class ABC revenue share donut chart.
- **Page 2 (Sales)**: Set up the Map visual mapping regional revenues, and a clustered column chart comparing Category Revenue against Freight.
- **Page 3 (Customer)**: Display customer growth trends and customer segment distributions.
- **Page 4 (Seller Scorecard)**: Use a Scatter Plot mapping Seller Revenue vs. Seller rating, alongside a searchable matrix of low-performing sellers.
- **Page 5 (Logistics)**: Plot lead time histograms and mapping LDR by customer state.
- **Page 6 (Review)**: Map rating distributions and display the searchable comment table visual.
