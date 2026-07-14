import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page layout
st.set_page_config(
    page_title="Olist E-Commerce C-Suite Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark-themed executive styling
st.markdown("""
<style>
    .reportview-container {
        background: #1E2229;
    }
    .metric-card {
        background-color: #2D3142;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        border-left: 5px solid #00A896;
        text-align: center;
    }
    .metric-value {
        font-size: 26px;
        font-weight: bold;
        color: #00A896;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 14px;
        color: #AEB3C2;
    }
</style>
""", unsafe_allowed_html=True)

# Helper function to load data
@st.cache_data
def load_dashboard_data():
    master_path = "data/processed/master_orders_dataset.csv"
    if not os.path.exists(master_path):
        return None
    df = pd.read_csv(master_path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

master_df = load_dashboard_data()

if master_df is None:
    st.error("Processed master dataset not found! Please run 'python src/run_feature_pipeline.py' first.")
    st.stop()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.image("https://raw.githubusercontent.com/olist/olist-dataset/master/olist.png", width=150)
st.sidebar.title("Dashboard Controls")

# Navigation Slicer
page = st.sidebar.radio(
    "Go to Page:",
    ["Executive Summary", "Sales Analysis", "Customer Analysis", "Seller Analysis", "Delivery Analysis", "Reviews Analysis"]
)

# Global Date Range Slicer
min_date = master_df['order_purchase_timestamp'].min().to_pydatetime()
max_date = master_df['order_purchase_timestamp'].max().to_pydatetime()
date_range = st.sidebar.slider(
    "Order Date Filter",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="MM/YY"
)

# Apply global date filter
filtered_df = master_df[
    (master_df['order_purchase_timestamp'] >= date_range[0]) &
    (master_df['order_purchase_timestamp'] <= date_range[1])
]

# State Filter Slicer
all_states = sorted(master_df['customer_state'].dropna().unique().tolist())
selected_states = st.sidebar.multiselect("Filter by Customer State:", all_states, default=None)
if selected_states:
    filtered_df = filtered_df[filtered_df['customer_state'].isin(selected_states)]

# ----------------- CALCULATE KPIs -----------------
total_revenue = filtered_df['revenue_per_order'].sum()
total_orders = filtered_df['order_id'].nunique()
total_customers = filtered_df['customer_unique_id'].nunique()
total_sellers = filtered_df['seller_id'].nunique()
aov = total_revenue / total_orders if total_orders > 0 else 0
avg_review = filtered_df['avg_review_score'].mean()
late_deliveries = (filtered_df['late_delivery_flag'] == 1).sum()
total_delivered = (filtered_df['order_status'] == 'delivered').sum()
ldr = (late_deliveries / total_delivered * 100) if total_delivered > 0 else 0
rpr = (filtered_df['repeat_customer_flag'] == 1).sum() / filtered_df['customer_unique_id'].nunique() * 100 if filtered_df['customer_unique_id'].nunique() > 0 else 0

# ----------------- PAGES -----------------
st.title(f"📊 Olist Executive Dashboard - {page}")

if page == "Executive Summary":
    # 1. Top Row Card Visuals
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Revenue (GMV)</div><div class="metric-value">{total_revenue/1e6:.2f}M BRL</div></div>', unsafe_allowed_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Orders</div><div class="metric-value">{total_orders/1e3:.1f}k</div></div>', unsafe_allowed_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Customers</div><div class="metric-value">{total_customers/1e3:.1f}k</div></div>', unsafe_allowed_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Average review rating</div><div class="metric-value">{avg_review:.2f} ★</div></div>', unsafe_allowed_html=True)
    with col5:
        st.markdown(f'<div class="metric-card" style="border-left-color: #F25F5C;"><div class="metric-label">Late Delivery Rate</div><div class="metric-value" style="color: #F25F5C;">{ldr:.2f}%</div></div>', unsafe_allowed_html=True)

    st.write("")
    
    # 2. Charts Section
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("Monthly Revenue (GMV) Growth")
        monthly_df = filtered_df.set_index('order_purchase_timestamp').resample('M').agg(
            revenue=('revenue_per_order', 'sum')
        ).reset_index()
        fig_monthly = px.line(monthly_df, x='order_purchase_timestamp', y='revenue', markers=True, template="plotly_dark", color_discrete_sequence=['#00A896'])
        fig_monthly.update_layout(yaxis_title="GMV (BRL)", xaxis_title="Purchase Month")
        st.plotly_chart(fig_monthly, use_container_width=True)
        
    with right_col:
        st.subheader("Payment Share by Type")
        pay_df = filtered_df['payment_category'].value_counts().reset_index()
        pay_df.columns = ['payment_type', 'count']
        fig_pie = px.pie(pay_df, names='payment_type', values='count', hole=0.4, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    # 3. Bottom State visual
    st.subheader("Top 10 States by Revenue (GMV)")
    state_df = filtered_df.groupby('customer_state')['revenue_per_order'].sum().reset_index().sort_values(by='revenue_per_order', ascending=False).head(10)
    fig_state = px.bar(state_df, x='revenue_per_order', y='customer_state', orientation='h', template="plotly_dark", color_discrete_sequence=['#00A896'])
    fig_state.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Revenue (BRL)")
    st.plotly_chart(fig_state, use_container_width=True)

elif page == "Sales Analysis":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Gross GMV</div><div class="metric-value">{total_revenue/1e6:.2f}M BRL</div></div>', unsafe_allowed_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Average Order Value (AOV)</div><div class="metric-value">{aov:.2f} BRL</div></div>', unsafe_allowed_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Freight Billing</div><div class="metric-value">{filtered_df["total_freight"].sum()/1e6:.2f}M BRL</div></div>', unsafe_allowed_html=True)

    st.write("")

    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("Product Category Sales Share (Class Pareto)")
        cat_df = filtered_df.groupby('product_category')['revenue_per_order'].sum().reset_index().sort_values(by='revenue_per_order', ascending=False).head(15)
        fig_cat = px.bar(cat_df, x='revenue_per_order', y='product_category', orientation='h', template="plotly_dark", color_discrete_sequence=['#00A896'])
        fig_cat.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with right_col:
        st.subheader("Order Split by Value Category")
        rev_cat = filtered_df['revenue_category'].value_counts().reset_index()
        rev_cat.columns = ['revenue_category', 'orders']
        fig_rev = px.pie(rev_cat, names='revenue_category', values='orders', template="plotly_dark")
        st.plotly_chart(fig_rev, use_container_width=True)

elif page == "Customer Analysis":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total Customers</div><div class="metric-value">{total_customers/1e3:.1f}k</div></div>', unsafe_allowed_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Repeat Purchase Rate (RPR)</div><div class="metric-value">{rpr:.2f}%</div></div>', unsafe_allowed_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">High-Value Customer Share</div><div class="metric-value">{(filtered_df["high_value_customer"] == 1).mean() * 100:.2f}%</div></div>', unsafe_allowed_html=True)

    st.write("")

    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("Customer Segment Distribution")
        seg_counts = filtered_df.groupby('customer_unique_id')['repeat_customer_flag'].first().value_counts().reset_index()
        seg_counts.columns = ['Buyer Type', 'Count']
        seg_counts['Buyer Type'] = seg_counts['Buyer Type'].map({1: 'Repeat Buyer', 0: 'One-off Buyer'})
        fig_seg = px.bar(seg_counts, x='Buyer Type', y='Count', template="plotly_dark", color='Buyer Type')
        st.plotly_chart(fig_seg, use_container_width=True)
        
    with right_col:
        st.subheader("Customer Value Split")
        hv_counts = filtered_df.groupby('customer_unique_id')['high_value_customer'].first().value_counts().reset_index()
        hv_counts.columns = ['Segment', 'Count']
        hv_counts['Segment'] = hv_counts['Segment'].map({1: 'High Spenders (Top 10%)', 0: 'Regular Spenders'})
        fig_hv = px.pie(hv_counts, names='Segment', values='Count', hole=0.3, template="plotly_dark", color_discrete_sequence=['#4F81BD', '#C0504D'])
        st.plotly_chart(fig_hv, use_container_width=True)

elif page == "Seller Analysis":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Active Sellers</div><div class="metric-value">{total_sellers}</div></div>', unsafe_allowed_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">State-matching transactions</div><div class="metric-value">{filtered_df["seller_state_match"].mean()*100:.2f}%</div></div>', unsafe_allowed_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Average Order Size</div><div class="metric-value">{filtered_df["order_size"].mean():.2f} items</div></div>', unsafe_allowed_html=True)

    st.write("")
    
    st.subheader("Underperforming Merchant List (Low review scores)")
    # Group by seller to show a table matrix of high-risk sellers
    seller_summary = filtered_df.groupby('seller_id').agg(
        orders=('order_id', 'nunique'),
        sales=('revenue_per_order', 'sum'),
        rating=('avg_review_score', 'mean'),
        late_rate=('late_delivery_flag', 'mean')
    ).reset_index()
    
    seller_summary['late_rate'] = (seller_summary['late_rate'] * 100).round(2)
    seller_summary['rating'] = seller_summary['rating'].round(2)
    seller_summary['sales'] = seller_summary['sales'].round(2)
    
    underperforming = seller_summary[
        (seller_summary['orders'] >= 10) & (seller_summary['rating'] < 3.5)
    ].sort_values(by='rating').head(10)
    
    st.dataframe(underperforming, use_container_width=True)

elif page == "Delivery Analysis":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Average Delivery Days</div><div class="metric-value">{filtered_df["delivery_days"].mean():.1f} Days</div></div>', unsafe_allowed_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #F25F5C;"><div class="metric-label">Late Delivery Rate (LDR)</div><div class="metric-value" style="color: #F25F5C;">{ldr:.2f}%</div></div>', unsafe_allowed_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Average Transit Delay</div><div class="metric-value">{filtered_df["delivery_delay"].dropna().mean():.1f} Days</div></div>', unsafe_allowed_html=True)

    st.write("")

    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("Distribution of actual delivery times (Days)")
        lead_time_df = filtered_df.dropna(subset=['delivery_days'])
        fig_hist = px.histogram(lead_time_df, x='delivery_days', nbins=50, template="plotly_dark", color_discrete_sequence=['#00A896'])
        fig_hist.update_layout(xaxis_title="Actual transit days", yaxis_title="Orders count", xaxis_range=[0, 45])
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with right_col:
        st.subheader("Late Delivery Rate by State")
        state_ldr = filtered_df.groupby('customer_state')['late_delivery_flag'].mean().reset_index()
        state_ldr['late_delivery_flag'] = state_ldr['late_delivery_flag'] * 100
        state_ldr = state_ldr.sort_values(by='late_delivery_flag', ascending=False).head(10)
        fig_ldr = px.bar(state_ldr, x='late_delivery_flag', y='customer_state', orientation='h', template="plotly_dark", color_discrete_sequence=['#F25F5C'])
        fig_ldr.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="LDR (%)")
        st.plotly_chart(fig_ldr, use_container_width=True)

elif page == "Reviews Analysis":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Average rating score</div><div class="metric-value">{avg_review:.2f} ★</div></div>', unsafe_allowed_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Positive Reviews Rate (4-5★)</div><div class="metric-value">{(filtered_df["review_category"]=="positive").mean()*100:.2f}%</div></div>', unsafe_allowed_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="border-left-color: #F25F5C;"><div class="metric-label">Negative Reviews Rate (1-2★)</div><div class="metric-value" style="color: #F25F5C;">{(filtered_df["review_category"]=="negative").mean()*100:.2f}%</div></div>', unsafe_allowed_html=True)

    st.write("")

    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("Customer Ratings Distribution")
        rating_counts = filtered_df['avg_review_score'].value_counts().reset_index()
        rating_counts.columns = ['score', 'count']
        rating_counts = rating_counts[rating_counts['score'] > 0].sort_values(by='score')
        fig_rating = px.bar(rating_counts, x='score', y='count', template="plotly_dark", color='score', color_continuous_scale=px.colors.sequential.RdBu)
        st.plotly_chart(fig_rating, use_container_width=True)
        
    with right_col:
        st.subheader("Star Rating vs. Delivery Delay")
        delay_review = filtered_df.groupby('avg_review_score')['delivery_delay'].mean().reset_index()
        delay_review = delay_review[delay_review['avg_review_score'] > 0]
        fig_delay = px.line(delay_review, x='avg_review_score', y='delivery_delay', markers=True, template="plotly_dark", color_discrete_sequence=['#F25F5C'])
        fig_delay.update_layout(xaxis_title="Star Rating score", yaxis_title="Average delivery delay (Days)")
        st.plotly_chart(fig_delay, use_container_width=True)
        
    # Search logs
    st.subheader("Customer Comments Keyword Search")
    review_comments = pd.read_csv("data/processed/olist_order_reviews_dataset.csv")
    search_query = st.text_input("Enter keyword (e.g. 'atraso', 'produto', 'ruim'):", "")
    if search_query:
        # filter comments
        matches = review_comments[
            review_comments['review_comment_message'].str.contains(search_query, case=False, na=False)
        ][['review_score', 'review_comment_message']].head(20)
        st.write(f"Showing top {len(matches)} matching comments:")
        st.dataframe(matches, use_container_width=True)
