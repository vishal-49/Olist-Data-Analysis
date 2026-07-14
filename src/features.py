import pandas as pd
import numpy as np

def build_master_features(orders_df, customers_df, items_df, payments_df, reviews_df, products_df, sellers_df):
    """
    Combines the cleaned datasets to build a unified Master Orders dataframe 
    with advanced business features:
    - Temporal features (month, year, quarter, weekday, weekend flag, hour)
    - Logistics metrics (delivery days, estimated delivery, delay days, transit duration, late flag)
    - Customer metrics (lifetime, order count, repeat flag, high-value flag)
    - Financial features (order size, average price, total spending, revenue categories)
    - Aggregated reviews and payment metrics
    """
    
    # 1. Prepare Datetime Columns in incoming DataFrames just in case
    orders = orders_df.copy()
    items = items_df.copy()
    payments = payments_df.copy()
    reviews = reviews_df.copy()
    customers = customers_df.copy()
    products = products_df.copy()
    sellers = sellers_df.copy()
    
    date_cols = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col])
        
    items['shipping_limit_date'] = pd.to_datetime(items['shipping_limit_date'])
    reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
    reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'])
    
    # 2. Aggregate Order Items
    # Join items with products and sellers to get category and location details
    items_enriched = items.merge(products[['product_id', 'product_category_name_english']], on='product_id', how='left')
    items_enriched = items_enriched.merge(sellers[['seller_id', 'seller_state', 'seller_city']], on='seller_id', how='left')
    
    items_agg = items_enriched.groupby('order_id').agg(
        order_size=('order_item_id', 'count'),
        total_price=('price', 'sum'),
        total_freight=('freight_value', 'sum'),
        avg_item_price=('price', 'mean'),
        seller_state=('seller_state', lambda x: x.iloc[0] if not x.empty else np.nan),
        seller_city=('seller_city', lambda x: x.iloc[0] if not x.empty else np.nan),
        product_category=('product_category_name_english', lambda x: x.iloc[0] if not x.empty else 'unknown')
    ).reset_index()
    
    items_agg['revenue_per_order'] = items_agg['total_price'] + items_agg['total_freight']
    
    # 3. Aggregate Payments
    def get_dominant_payment(x):
        if x.empty:
            return 'unknown'
        return x.mode().iloc[0]
        
    payments_agg = payments.groupby('order_id').agg(
        payment_value_sum=('payment_value', 'sum'),
        payment_installments=('payment_installments', 'max'),
        payment_category=('payment_type', get_dominant_payment)
    ).reset_index()
    
    # 4. Aggregate Reviews
    reviews_agg = reviews.groupby('order_id').agg(
        avg_review_score=('review_score', 'mean'),
        review_count=('review_id', 'count')
    ).reset_index()
    
    # Map review categories based on score
    def categorize_review(score):
        if pd.isnull(score):
            return 'unknown'
        if score >= 4.0:
            return 'positive'
        elif score == 3.0:
            return 'neutral'
        else:
            return 'negative'
            
    reviews_agg['review_category'] = reviews_agg['avg_review_score'].apply(categorize_review)
    
    # 5. Build Master Dataset by Merging
    master = orders.merge(customers, on='customer_id', how='left')
    master = master.merge(items_agg, on='order_id', how='left')
    master = master.merge(payments_agg, on='order_id', how='left')
    master = master.merge(reviews_agg, on='order_id', how='left')
    
    # Fill NaN for orders without items/payments/reviews
    master['order_size'] = master['order_size'].fillna(0).astype(int)
    master['total_price'] = master['total_price'].fillna(0)
    master['total_freight'] = master['total_freight'].fillna(0)
    master['revenue_per_order'] = master['revenue_per_order'].fillna(0)
    master['avg_item_price'] = master['avg_item_price'].fillna(0)
    master['payment_value_sum'] = master['payment_value_sum'].fillna(0)
    master['payment_installments'] = master['payment_installments'].fillna(1).astype(int)
    master['payment_category'] = master['payment_category'].fillna('unknown')
    master['avg_review_score'] = master['avg_review_score'].fillna(0)
    master['review_category'] = master['review_category'].fillna('unknown')
    master['product_category'] = master['product_category'].fillna('unknown')
    
    # 6. Temporal Features
    master['order_year'] = master['order_purchase_timestamp'].dt.year
    master['order_month'] = master['order_purchase_timestamp'].dt.month
    master['order_quarter'] = master['order_purchase_timestamp'].dt.quarter
    master['order_weekday'] = master['order_purchase_timestamp'].dt.weekday
    master['weekend_order'] = master['order_weekday'].apply(lambda x: 1 if x in [5, 6] else 0)
    master['purchase_hour'] = master['order_purchase_timestamp'].dt.hour
    
    # 7. Logistics Features
    master['delivery_days'] = (master['order_delivered_customer_date'] - master['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
    master['estimated_delivery_days'] = (master['order_estimated_delivery_date'] - master['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
    master['delivery_delay'] = (master['order_delivered_customer_date'] - master['order_estimated_delivery_date']).dt.total_seconds() / (24 * 3600)
    master['shipping_duration'] = (master['order_delivered_customer_date'] - master['order_delivered_carrier_date']).dt.total_seconds() / (24 * 3600)
    
    # Late Delivery Flag
    # Set to 1 if actual delivery date is greater than estimated delivery date, else 0
    # If not delivered yet, check if current time is past estimate, but standard behavior is based on completed deliveries
    master['late_delivery_flag'] = 0
    master.loc[master['delivery_delay'] > 0, 'late_delivery_flag'] = 1
    
    # 8. Customer Loyalty & Retention Features
    # Group by customer_unique_id to calculate lifetime metrics
    customer_stats = master.groupby('customer_unique_id').agg(
        customer_total_orders=('order_id', 'nunique'),
        customer_total_spend=('revenue_per_order', 'sum'),
        first_purchase_date=('order_purchase_timestamp', 'min')
    ).reset_index()
    
    # Merge customer stats back
    master = master.merge(customer_stats, on='customer_unique_id', how='left')
    
    # Customer lifetime in days at time of purchase
    master['customer_lifetime'] = (master['order_purchase_timestamp'] - master['first_purchase_date']).dt.total_seconds() / (24 * 3600)
    
    # Repeat Customer Flag
    master['repeat_customer_flag'] = (master['customer_total_orders'] > 1).astype(int)
    
    # High-Value Customer Flag (based on top 10% spending)
    threshold_spend = master['customer_total_spend'].quantile(0.90)
    master['high_value_customer'] = (master['customer_total_spend'] >= threshold_spend).astype(int)
    
    # 9. Revenue Category
    # Categorize order revenue: Low (<50 BRL), Medium (50-200 BRL), High (>200 BRL)
    def categorize_revenue(val):
        if val < 50.0:
            return 'low'
        elif val <= 200.0:
            return 'medium'
        else:
            return 'high'
            
    master['revenue_category'] = master['revenue_per_order'].apply(categorize_revenue)
    
    # 10. Geography matches
    master['seller_state_match'] = (master['customer_state'] == master['seller_state']).astype(int)
    
    return master
