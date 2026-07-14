import os
import sys
import pandas as pd
import numpy as np

# Set path relative to project root
sys.path.append(os.path.abspath("."))
from src.features import build_master_features

PROCESSED_DIR = "data/processed"

print("Loading processed files...")
customers = pd.read_csv(os.path.join(PROCESSED_DIR, "olist_customers_dataset.csv"))
order_items = pd.read_csv(os.path.join(PROCESSED_DIR, "olist_order_items_dataset.csv"))
order_payments = pd.read_csv(os.path.join(PROCESSED_DIR, "olist_order_payments_dataset.csv"))
order_reviews = pd.read_csv(os.path.join(PROCESSED_DIR, "olist_order_reviews_dataset.csv"))
orders = pd.read_csv(os.path.join(PROCESSED_DIR, "olist_orders_dataset.csv"))
products = pd.read_csv(os.path.join(PROCESSED_DIR, "olist_products_dataset.csv"))
sellers = pd.read_csv(os.path.join(PROCESSED_DIR, "olist_sellers_dataset.csv"))

print("Building master orders table and extracting features...")
master_orders = build_master_features(
    orders_df=orders,
    customers_df=customers,
    items_df=order_items,
    payments_df=order_payments,
    reviews_df=order_reviews,
    products_df=products,
    sellers_df=sellers
)

print(f"Master dataset built with shape {master_orders.shape}.")
print("Exporting master dataset...")
master_orders.to_csv(os.path.join(PROCESSED_DIR, "master_orders_dataset.csv"), index=False)
print("Feature engineering pipeline completed successfully!")
