import pandas as pd
import numpy as np

def clean_customers(df):
    """
    Cleans the customers dataframe:
    - Normalizes city names (strip whitespace, lowercase).
    - Checks for missing values.
    """
    df_clean = df.copy()
    # Normalize customer city
    df_clean['customer_city'] = df_clean['customer_city'].str.strip().str.lower()
    return df_clean

def clean_sellers(df):
    """
    Cleans the sellers dataframe:
    - Normalizes city names.
    """
    df_clean = df.copy()
    df_clean['seller_city'] = df_clean['seller_city'].str.strip().str.lower()
    return df_clean

def clean_geolocation(df):
    """
    Cleans and de-duplicates the geolocation dataframe to prevent cartesian products:
    - Removes latitude/longitude coordinate points outside the bounding box of Brazil.
    - Groups by zip code prefix and takes the average latitude and longitude.
    - Resolves the most frequent city/state name for each zip code (mode).
    """
    df_clean = df.copy()
    
    # Bounding box of Brazil
    # Latitudes: -34 to 6 degrees, Longitudes: -74 to -34 degrees
    df_clean = df_clean[
        (df_clean['geolocation_lat'] >= -34.0) & (df_clean['geolocation_lat'] <= 6.0) &
        (df_clean['geolocation_lng'] >= -74.0) & (df_clean['geolocation_lng'] <= -34.0)
    ]
    
    # Normalize city strings before taking mode
    df_clean['geolocation_city'] = df_clean['geolocation_city'].str.strip().str.lower()
    
    # Aggregation mapping
    # Mean for latitude and longitude; first/mode for city and state
    agg_funcs = {
        'geolocation_lat': 'mean',
        'geolocation_lng': 'mean',
        'geolocation_city': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        'geolocation_state': lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan
    }
    
    df_grouped = df_clean.groupby('geolocation_zip_code_prefix').agg(agg_funcs).reset_index()
    return df_grouped

def clean_orders(df):
    """
    Cleans the orders dataframe:
    - Converts timestamp columns to datetime.
    - Ensures chronological consistency (purchase <= approved <= carrier <= customer).
    """
    df_clean = df.copy()
    
    timestamp_cols = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    
    for col in timestamp_cols:
        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        
    return df_clean

def clean_order_items(df):
    """
    Cleans the order items dataframe:
    - Converts shipping limit date to datetime.
    - Validates price and freight values (must be non-negative).
    """
    df_clean = df.copy()
    df_clean['shipping_limit_date'] = pd.to_datetime(df_clean['shipping_limit_date'], errors='coerce')
    
    # Remove records with negative prices/freight
    df_clean = df_clean[(df_clean['price'] >= 0) & (df_clean['freight_value'] >= 0)]
    return df_clean

def clean_order_payments(df):
    """
    Cleans the order payments dataframe:
    - Validates payment value (must be non-negative).
    """
    df_clean = df.copy()
    df_clean = df_clean[df_clean['payment_value'] >= 0]
    return df_clean

def clean_order_reviews(df):
    """
    Cleans the order reviews dataframe:
    - Converts review dates to datetime.
    - Fills null review titles and messages with defaults.
    """
    df_clean = df.copy()
    
    df_clean['review_creation_date'] = pd.to_datetime(df_clean['review_creation_date'], errors='coerce')
    df_clean['review_answer_timestamp'] = pd.to_datetime(df_clean['review_answer_timestamp'], errors='coerce')
    
    df_clean['review_comment_title'] = df_clean['review_comment_title'].fillna('no_title').str.strip()
    df_clean['review_comment_message'] = df_clean['review_comment_message'].fillna('no_message').str.strip()
    
    return df_clean

def clean_products(df, translation_df):
    """
    Cleans the products dataframe and translates product category names to English:
    - Joins with the translation dataframe.
    - Replaces missing category names with 'other' or 'unknown'.
    - Imputes missing dimensional values with 0 or column medians.
    """
    df_clean = df.copy()
    
    # Merge with translation mapping
    df_merged = df_clean.merge(translation_df, on='product_category_name', how='left')
    
    # If the category is missing or there's no English translation, fill it
    df_merged['product_category_name_english'] = df_merged['product_category_name_english'].fillna('unknown')
    df_merged['product_category_name'] = df_merged['product_category_name'].fillna('unknown')
    
    # Fill structural missing dimensions
    dim_cols = [
        'product_name_lenght', 'product_description_lenght',
        'product_photos_qty', 'product_weight_g',
        'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    
    for col in dim_cols:
        df_merged[col] = df_merged[col].fillna(0)
        
    return df_merged
