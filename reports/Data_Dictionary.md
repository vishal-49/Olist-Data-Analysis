# Olist Brazilian E-Commerce Data Dictionary

This document serves as the official data dictionary for the Olist E-Commerce dataset, defining the tables, columns, primary keys, foreign keys, and descriptions.

---

## 1. Table Definitions

### 1.1 Customers Table (`olist_customers_dataset.csv`)
Contains customer location details. A customer has a unique `customer_id` for every order, but their overall customer identity is captured by `customer_unique_id`.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | VARCHAR | PK | Order-level customer key. Links to `FactOrders`. |
| `customer_unique_id` | VARCHAR | - | Unique customer identifier (remains constant across purchases). |
| `customer_zip_code_prefix` | INTEGER | FK | First 5 digits of customer zip code. Links to `DimGeolocation`. |
| `customer_city` | VARCHAR | - | City name. |
| `customer_state` | VARCHAR | - | State code (e.g., SP, RJ). |

---

### 1.2 Geolocation Table (`olist_geolocation_dataset.csv`)
Contains spatial coordinates mapping zip code prefixes to latitude/longitude centroids.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `geolocation_zip_code_prefix` | INTEGER | PK/FK | First 5 digits of zip code. |
| `geolocation_lat` | DOUBLE | - | Latitude coordinate centroid. |
| `geolocation_lng` | DOUBLE | - | Longitude coordinate centroid. |
| `geolocation_city` | VARCHAR | - | Normalized city name. |
| `geolocation_state` | VARCHAR | - | Normalized state code. |

---

### 1.3 Order Items Table (`olist_order_items_dataset.csv`)
Tracks line-item details for each order transaction.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR | FK | Unique order identifier. Links to `FactOrders`. |
| `order_item_id` | INTEGER | PK | Sequential integer identifying items in the same order. |
| `product_id` | VARCHAR | FK | Product identifier. Links to `DimProducts`. |
| `seller_id` | VARCHAR | FK | Seller identifier. Links to `DimSellers`. |
| `shipping_limit_date` | TIMESTAMP | - | Date by which the seller must hand over the package to carrier. |
| `price` | DOUBLE | - | Unit selling price. |
| `freight_value` | DOUBLE | - | Shipping fee per unit. |

---

### 1.4 Order Payments Table (`olist_order_payments_dataset.csv`)
Tracks payment transaction details. Multiple rows can exist per order if split payments are used.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR | FK | Unique order identifier. Links to `FactOrders`. |
| `payment_sequential` | INTEGER | PK | Sequential count for split payment methods. |
| `payment_type` | VARCHAR | - | Method used (credit_card, debit_card, voucher, boleto). |
| `payment_installments` | INTEGER | - | Selected credit card installments count. |
| `payment_value` | DOUBLE | - | Total payment transaction value. |

---

### 1.5 Order Reviews Table (`olist_order_reviews_dataset.csv`)
Tracks customer review ratings and written feedback.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `review_id` | VARCHAR | PK | Unique review identifier. |
| `order_id` | VARCHAR | FK | Unique order identifier. Links to `FactOrders`. |
| `review_score` | INTEGER | - | Rating from 1 (lowest) to 5 (highest). |
| `review_comment_title` | VARCHAR | - | Title of review text comment (defaulted to 'no_title' if null). |
| `review_comment_message` | VARCHAR | - | Written review message (defaulted to 'no_message' if null). |
| `review_creation_date` | TIMESTAMP | - | Date the survey was sent. |
| `review_answer_timestamp` | TIMESTAMP | - | Timestamp of customer submission. |

---

### 1.6 Orders Table (`olist_orders_dataset.csv`)
The central transaction table tracking states and logistics timestamps.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | VARCHAR | PK | Unique order identifier. |
| `customer_id` | VARCHAR | FK | Order-level customer key. Links to `DimCustomers`. |
| `order_status` | VARCHAR | - | State of transaction (delivered, shipped, canceled, etc.). |
| `order_purchase_timestamp` | TIMESTAMP | - | Date and time order was placed. |
| `order_approved_at` | TIMESTAMP | - | Timestamp of payment approval. |
| `order_delivered_carrier_date` | TIMESTAMP | - | Timestamp carrier picked up package. |
| `order_delivered_customer_date` | TIMESTAMP | - | Timestamp package reached customer. |
| `order_estimated_delivery_date`| TIMESTAMP | - | Estimated delivery date promised by Olist. |

---

### 1.7 Products Table (`olist_products_dataset.csv`)
Contains product descriptions and physical characteristics.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | VARCHAR | PK | Unique product identifier. |
| `product_category_name` | VARCHAR | FK | Category name in Portuguese. Links to translation table. |
| `product_category_name_english`| VARCHAR | - | Translated English category name (defaulted to 'unknown'). |
| `product_weight_g` | DOUBLE | - | Product weight in grams. |
| `product_length_cm` | DOUBLE | - | Product length in cm. |
| `product_height_cm` | DOUBLE | - | Product height in cm. |
| `product_width_cm` | DOUBLE | - | Product width in cm. |

---

### 1.8 Sellers Table (`olist_sellers_dataset.csv`)
Contains seller geographic data.

| Column | Physical Type | Key | Description |
| :--- | :--- | :--- | :--- |
| `seller_id` | VARCHAR | PK | Unique seller identifier. |
| `seller_zip_code_prefix` | INTEGER | FK | First 5 digits of seller zip code. Links to `DimGeolocation`. |
| `seller_city` | VARCHAR | - | Normalized seller city. |
| `seller_state` | VARCHAR | - | Seller state code. |
