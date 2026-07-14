import os
import sys
import pandas as pd
import numpy as np

# Set path relative to project root
sys.path.append(os.path.abspath("."))
from src.cleaning import (
    clean_customers,
    clean_sellers,
    clean_geolocation,
    clean_orders,
    clean_order_items,
    clean_order_payments,
    clean_order_reviews,
    clean_products
)

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("Loading raw files...")
customers_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_customers_dataset.csv"))
geolocation_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_geolocation_dataset.csv"))
order_items_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_order_items_dataset.csv"))
order_payments_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_order_payments_dataset.csv"))
order_reviews_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_order_reviews_dataset.csv"))
orders_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_orders_dataset.csv"))
products_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_products_dataset.csv"))
sellers_raw = pd.read_csv(os.path.join(RAW_DIR, "olist_sellers_dataset.csv"))
category_translation = pd.read_csv(os.path.join(RAW_DIR, "product_category_name_translation.csv"))

print("Cleaning customers...")
customers_clean = clean_customers(customers_raw)
customers_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_customers_dataset.csv"), index=False)

print("Cleaning sellers...")
sellers_clean = clean_sellers(sellers_raw)
sellers_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_sellers_dataset.csv"), index=False)

print("Cleaning geolocation (aggregating zip codes)...")
geolocation_clean = clean_geolocation(geolocation_raw)
geolocation_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_geolocation_dataset.csv"), index=False)

print("Cleaning orders...")
orders_clean = clean_orders(orders_raw)
orders_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_orders_dataset.csv"), index=False)

print("Cleaning order items...")
order_items_clean = clean_order_items(order_items_raw)
order_items_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_order_items_dataset.csv"), index=False)

print("Cleaning order payments...")
order_payments_clean = clean_order_payments(order_payments_raw)
order_payments_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_order_payments_dataset.csv"), index=False)

print("Cleaning reviews...")
order_reviews_clean = clean_order_reviews(order_reviews_raw)
order_reviews_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_order_reviews_dataset.csv"), index=False)

print("Cleaning products...")
products_clean = clean_products(products_raw, category_translation)
products_clean.to_csv(os.path.join(PROCESSED_DIR, "olist_products_dataset.csv"), index=False)

print("All files cleaned and exported successfully!")
