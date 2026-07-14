import pandas as pd
import numpy as np

def calculate_rfm(df):
    """
    Computes Recency, Frequency, and Monetary scores for each customer_unique_id:
    - Recency: Days since last order relative to the maximum date in the dataset.
    - Frequency: Total orders per customer.
    - Monetary: Total spending per customer.
    - Scores R, F, M on a scale of 1 to 5.
    - Segments customers into strategic groups.
    """
    # Use max purchase date + 1 day as the reference date
    max_date = pd.to_datetime(df['order_purchase_timestamp']).max()
    ref_date = max_date + pd.Timedelta(days=1)
    
    # Calculate R, F, M metrics
    rfm = df.groupby('customer_unique_id').agg(
        recency=('order_purchase_timestamp', lambda x: (ref_date - pd.to_datetime(x).max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('revenue_per_order', 'sum')
    ).reset_index()
    
    # R score: Lower recency is better -> higher score
    rfm['R'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1])
    
    # F score: Higher frequency is better. Due to highly skewed e-commerce frequency 
    # (most buyers buy 1 time), we assign manual thresholds to avoid overlapping bin bounds
    def score_frequency(x):
        if x == 1:
            return 1
        elif x == 2:
            return 3
        elif x == 3:
            return 4
        else:
            return 5
            
    rfm['F'] = rfm['frequency'].apply(score_frequency)
    
    # M score: Higher spending is better -> higher score
    rfm['M'] = pd.qcut(rfm['monetary'], q=5, labels=[1, 2, 3, 4, 5])
    
    # Convert scores to numeric
    rfm['R'] = rfm['R'].astype(int)
    rfm['F'] = rfm['F'].astype(int)
    rfm['M'] = rfm['M'].astype(int)
    
    # Combine score
    rfm['rfm_score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)
    
    # Segment customers
    def segment_rfm(row):
        r, f, m = row['R'], row['F'], row['M']
        if r >= 4 and f >= 4 and m >= 4:
            return 'Champions'
        elif r >= 3 and f >= 3 and m >= 3:
            return 'Loyal Customers'
        elif r >= 4 and f == 1:
            return 'New Customers'
        elif r >= 3 and f >= 1 and m >= 4:
            return 'High Spenders'
        elif r <= 2 and f >= 3 and m >= 4:
            return 'Can\'t Lose Them'
        elif r <= 2 and r >= 1 and f >= 1:
            return 'Hibernating / Lost'
        else:
            return 'About to Sleep'
            
    rfm['customer_segment'] = rfm.apply(segment_rfm, axis=1)
    return rfm

def calculate_abc_pareto(df, col_name='product_category'):
    """
    Applies the Pareto Principle (80/20 rule) to classify product categories:
    - Computes total revenue per category.
    - Calculates % and cumulative % of revenue.
    - Classifies categories into:
      - Class A: Top 80% of revenue (core drivers).
      - Class B: Next 15% (secondary).
      - Class C: Bottom 5% (long-tail).
    """
    cat_rev = df.groupby(col_name)['revenue_per_order'].sum().reset_index()
    cat_rev = cat_rev.sort_values(by='revenue_per_order', ascending=False)
    
    total_rev = cat_rev['revenue_per_order'].sum()
    cat_rev['rev_pct'] = cat_rev['revenue_per_order'] / total_rev
    cat_rev['cum_rev_pct'] = cat_rev['rev_pct'].cumsum()
    
    def assign_abc(cum_pct):
        if cum_pct <= 0.80:
            return 'A'
        elif cum_pct <= 0.95:
            return 'B'
        else:
            return 'C'
            
    cat_rev['abc_class'] = cat_rev['cum_rev_pct'].apply(assign_abc)
    return cat_rev

def calculate_cohort_retention(df):
    """
    Performs cohort analysis tracking monthly user retention:
    - Identifies first purchase month (CohortMonth) for each customer_unique_id.
    - Identifies purchase month (OrderMonth) for each order.
    - Calculates cohort index (months since first purchase).
    - Pivots into a cohort retention table.
    """
    temp = df.copy()
    temp['order_purchase_timestamp'] = pd.to_datetime(temp['order_purchase_timestamp'])
    
    # 1. Define order month
    temp['order_month_period'] = temp['order_purchase_timestamp'].dt.to_period('M')
    
    # 2. Define first purchase month (cohort month)
    temp['cohort_month_period'] = temp.groupby('customer_unique_id')['order_month_period'].transform('min')
    
    # 3. Calculate cohort index
    # We convert periods to integers to calculate month offsets
    temp['cohort_index'] = (temp['order_month_period'] - temp['cohort_month_period']).apply(lambda x: x.n)
    
    # 4. Group by cohort and cohort index
    cohort_data = temp.groupby(['cohort_month_period', 'cohort_index']).agg(
        unique_customers=('customer_unique_id', 'nunique')
    ).reset_index()
    
    # Pivot
    cohort_pivot = cohort_data.pivot(index='cohort_month_period', columns='cohort_index', values='unique_customers')
    
    # Convert index to string for plotting
    cohort_pivot.index = cohort_pivot.index.astype(str)
    
    # Calculate percentages
    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_sizes, axis=0)
    
    return cohort_pivot, retention_matrix

def calculate_seller_scorecard(items_df, reviews_df, orders_df):
    """
    Generates a quantitative scorecard for each seller:
    - Total GMV (sales).
    - Average Review Score.
    - Late Delivery Rate (LDR).
    - Computes a composite Seller Performance Score from 0 to 100.
    """
    # Enrich items with review score and delivery details
    orders_enrich = orders_df[['order_id', 'order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']]
    items_enrich = items_df.merge(orders_enrich, on='order_id', how='inner')
    
    # Calculate delay per item
    items_enrich['order_delivered_customer_date'] = pd.to_datetime(items_enrich['order_delivered_customer_date'])
    items_enrich['order_estimated_delivery_date'] = pd.to_datetime(items_enrich['order_estimated_delivery_date'])
    
    items_enrich['item_delay'] = (items_enrich['order_delivered_customer_date'] - items_enrich['order_estimated_delivery_date']).dt.total_seconds() / (24 * 3600)
    items_enrich['item_late'] = (items_enrich['item_delay'] > 0).astype(int)
    
    # Join with reviews
    reviews_agg = reviews_df.groupby('order_id')['review_score'].mean().reset_index()
    items_enrich = items_enrich.merge(reviews_agg, on='order_id', how='left')
    
    # Seller stats
    seller_stats = items_enrich.groupby('seller_id').agg(
        total_sales=('price', 'sum'),
        total_orders=('order_id', 'nunique'),
        avg_rating=('review_score', 'mean'),
        late_items_count=('item_late', 'sum'),
        total_items=('order_item_id', 'count')
    ).reset_index()
    
    seller_stats['late_delivery_rate'] = seller_stats['late_items_count'] / seller_stats['total_items']
    seller_stats['avg_rating'] = seller_stats['avg_rating'].fillna(4.0)  # fill with platform mode/median
    
    # Composite Score Formula: 
    # Score = 0.40 * RatingScore (Rating out of 5 mapped to 100) 
    #       + 0.40 * LogisticsScore (100 * (1 - LateDeliveryRate))
    #       + 0.20 * VolumeScore (log scaled Sales percentile score)
    
    # Normalize rating to 0-100 scale
    rating_score = (seller_stats['avg_rating'] / 5.0) * 100
    
    # Normalize logistics (late delivery rate)
    logistics_score = (1 - seller_stats['late_delivery_rate']) * 100
    
    # Volume score based on percentile rank of log sales
    sales_rank = seller_stats['total_sales'].rank(pct=True) * 100
    
    seller_stats['performance_score'] = (
        0.40 * rating_score + 
        0.40 * logistics_score + 
        0.20 * sales_rank
    ).round(1)
    
    return seller_stats.sort_values(by='performance_score', ascending=False)
