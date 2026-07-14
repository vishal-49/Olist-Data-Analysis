# Power BI DAX Measures & Data Model Documentation

This document defines the data model relationships, calculated tables, calculated columns, and DAX measures required to build the executive Power BI dashboard.

---

## 1. Data Model Relationships (Star Schema)

To ensure optimal performance, the model should follow a **Star Schema** with `master_orders_dataset` (or a combination of orders and order items) as the central fact table.

- **`FactOrders`** (`master_orders_dataset.csv`)
- **`DimCustomers`** (`olist_customers_dataset.csv`) joined to `FactOrders` on `customer_unique_id` (1:N) or `customer_id` (1:1)
- **`DimSellers`** (`olist_sellers_dataset.csv`) joined to `FactOrders` on `seller_id` (1:N)
- **`DimProducts`** (`olist_products_dataset.csv`) joined to `FactOrders` on `product_id` (1:N)
- **`DimDate`** (Calculated Table) joined to `FactOrders` on `order_purchase_timestamp` (1:N)

---

## 2. Calculated Tables

### 2.1 Calendar Table (`DimDate`)
Creates a standard, continuous calendar table for Time Intelligence calculations.
```dax
DimDate = 
VAR MinDate = MIN(FactOrders[order_purchase_timestamp])
VAR MaxDate = MAX(FactOrders[order_purchase_timestamp])
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "MonthNum", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "MonthYear", FORMAT([Date], "MMM YYYY"),
    "MonthYearSort", YEAR([Date]) * 100 + MONTH([Date]),
    "Weekday", FORMAT([Date], "dddd"),
    "WeekdayNum", WEEKDAY([Date], 2),
    "IsWeekend", IF(WEEKDAY([Date], 2) >= 6, "Weekend", "Weekday")
)
```
*Note: Sort the `MonthYear` column by `MonthYearSort` to ensure correct chronological rendering in visual charts.*

---

## 3. Key Performance Indicator (KPI) Measures

### 3.1 Total Revenue (GMV)
Calculates total gross merchandise value.
```dax
Total Revenue = SUM(FactOrders[revenue_per_order])
```

### 3.2 Total Orders
Calculates the count of unique transactions.
```dax
Total Orders = DISTINCTCOUNT(FactOrders[order_id])
```

### 3.3 Total Customers
Calculates the count of unique consumer profiles.
```dax
Total Customers = DISTINCTCOUNT(FactOrders[customer_unique_id])
```

### 3.4 Total Sellers
Calculates active sellers.
```dax
Total Sellers = DISTINCTCOUNT(FactOrders[seller_id])
```

### 3.5 Average Order Value (AOV)
```dax
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

### 3.6 Average Delivery Days
```dax
Average Delivery Days = AVERAGE(FactOrders[delivery_days])
```

### 3.7 Average Review Score
```dax
Average Review Score = AVERAGE(FactOrders[avg_review_score])
```

### 3.8 Late Delivery Rate (LDR)
Computes the percentage of orders delivered past the estimated date.
```dax
Late Delivery Rate = 
DIVIDE(
    CALCULATE([Total Orders], FactOrders[late_delivery_flag] = 1),
    CALCULATE([Total Orders], NOT(ISBLANK(FactOrders[order_delivered_customer_date]))),
    0
)
```

### 3.9 Repeat Purchase Rate (RPR)
```dax
Repeat Purchase Rate = 
VAR CustomersWithMultipleOrders = 
    COUNTROWS(
        FILTER(
            VALUES(FactOrders[customer_unique_id]),
            CALCULATE(DISTINCTCOUNT(FactOrders[order_id])) > 1
        )
    )
VAR TotalActiveCustomers = [Total Customers]
RETURN
    DIVIDE(CustomersWithMultipleOrders, TotalActiveCustomers, 0)
```

---

## 4. Time Intelligence & Growth Measures

### 4.1 Year-to-Date (YTD) Revenue
```dax
Revenue YTD = TOTALYTD([Total Revenue], DimDate[Date])
```

### 4.2 Prior Month Sales (MoM Comparison)
```dax
Prior Month Revenue = CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH))
```

### 4.3 Month-over-Month (MoM) Growth Percentage
```dax
MoM Revenue Growth % = 
VAR CurrentRev = [Total Revenue]
VAR PriorRev = [Prior Month Revenue]
RETURN
    DIVIDE(CurrentRev - PriorRev, PriorRev, 0)
```

### 4.4 Prior Year Sales (YoY Comparison)
```dax
Prior Year Revenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))
```

### 4.5 Year-over-Year (YoY) Growth Percentage
```dax
YoY Revenue Growth % = 
VAR CurrentRev = [Total Revenue]
VAR PriorRev = [Prior Year Revenue]
RETURN
    DIVIDE(CurrentRev - PriorRev, PriorRev, 0)
```

---

## 5. Calculated Columns (FactOrders)

### 5.1 Delivery Status Bins
Borders the order delay days into user-friendly status updates.
```dax
Delivery Status = 
IF(
    ISBLANK(FactOrders[order_delivered_customer_date]),
    "In Transit / Pending",
    IF(
        FactOrders[delivery_delay] > 0,
        "Late Delivery",
        "On-Time / Early"
    )
)
```

### 5.2 Dynamic Customer RFM Segments
Recreates segments inside Power BI for slicing visuals.
```dax
PowerBI_Customer_Segment = 
SWITCH(
    TRUE(),
    FactOrders[repeat_customer_flag] = 1 && FactOrders[high_value_customer] = 1, "VIP Champions",
    FactOrders[repeat_customer_flag] = 1 && FactOrders[high_value_customer] = 0, "Loyal Mid-Tier",
    FactOrders[repeat_customer_flag] = 0 && FactOrders[high_value_customer] = 1, "New High Spenders",
    "One-Off Regular Buyers"
)
```
