# Olist Brazilian E-Commerce Executive Report
**Prepared for**: Olist Executive Leadership Team  
**Date**: July 2026  
**Author**: Lead Data Analytics Consultant

---

## 1. Executive Summary

Olist operates a fast-growing, multi-tenant marketplace platform that connects small and medium-sized merchants across Brazil to national retail channels. While sales velocity and Gross Merchandise Value (GMV) have shown strong upward momentum—growing from 130K BRL to over 1.0M BRL monthly GMV from early 2017 to mid-2018—operational scaling bottlenecks threaten platform-wide Net Promoter Scores (NPS), merchant retention, and customer lifetime value.

This report evaluates operational friction across three core pillars: logistics performance, customer satisfaction, and payment checkout conversions. It outlines a data-driven path forward to reduce delivery delays, increase customer repeat purchase rates, and establish merchant compliance standards.

---

## 2. Platform KPI Dashboard

Our analysis establishes the following baseline operational and financial performance indicators for Olist:

| Metric | Baseline Value | Status | Target | Strategic Action Item |
| :--- | :--- | :--- | :--- | :--- |
| **Total Revenue (GMV)** | **~15.9M BRL** | 🟢 Healthy | +15% YoY | Optimize Southeast advertising spend. |
| **Average Order Value (AOV)** | **160.2 BRL** | 🟡 Stable | +5% YoY | Offer interest-free installment promotions. |
| **Late Delivery Rate (LDR)** | **~6.6%** | 🔴 Critical | < 5.0% | Audit carriers in slow northern states. |
| **Median Delivery Time** | **10.2 Days** | 🟡 Moderate | < 8.0 Days | Establish regional fulfillment hubs (Olist Envios). |
| **Average Review Rating** | **4.08 / 5.0** | 🟡 Stable | > 4.2 / 5.0 | Implement Seller Scorecard compliance. |
| **Repeat Purchase Rate (RPR)**| **~3.2%** | 🔴 Critical | > 6.0% | Deploy post-purchase loyalty coupons. |

---

## 3. Key Analytical Findings

1. **Logistics is the Primary Driver of Negative Reviews**: Nearly **37%** of negative customer feedback (1 and 2 stars) is caused by late deliveries. Orders delivered late drop the average review rating from **4.3** down to **2.2**, severely damaging Olist's search ranking on partner marketplaces.
2. **Extreme Customer Acquisition Dependence**: Cohort retention analysis reveals a retention rate below **0.5%** in Month 1 across nearly all monthly cohorts. Olist is operating as a transactional destination rather than a sticky, repeating customer ecosystem.
3. **Southeast Sales Concentration**: Over **60%** of total platform GMV is concentrated in the Southeast region (SP, RJ, MG, ES), with São Paulo alone accounting for **37%** of sales.
4. **Installment Leverage**: Credit cards are the preferred payment option, representing **73%** of checkouts. Customers using installments buy substantially larger ticket sizes (higher AOV), proving that flexible credit terms drive overall basket size.
5. **Class A Categories**: The Pareto Principle holds true for the platform: **only 15 product categories (out of 72) generate 80% of sales**, with Health & Beauty, Watches & Gifts, and Bed & Bath & Table heading the list.

---

## 4. Strategic Recommendations

Based on these findings, we recommend the following executive initiatives:

1. **Centralize Southeast Warehousing (Olist Envios)**: Establish physical fulfillment centers in the São Paulo metro area. Pre-stocking Class A items will decrease median transit times from 10.2 days down to 2 days for SP customers, lowering shipping costs and LDR.
2. **Seller Scorecard Compliance**: Deploy our composite Seller Scorecard to enforce SLAs. Sellers with scores below 50 should face search-ranking demotions until their late fulfillment rates fall below 5%.
3. **Launch Post-Purchase CRM Triggers**: Address the 3.2% Repeat Purchase Rate by offering a 10% discount voucher valid for 30 days, sent automatically via email once an order is marked as successfully delivered.
4. **Interest-Free Installment Co-Marketing**: Partner with credit card processors to offer up to 6 interest-free installments for Class A product purchases. This will raise overall AOV while mitigating consumer cash-flow restrictions.
5. **Dynamic Estimated Delivery Dates**: Replace static estimate formulas with state-specific carrier matrices. Setting realistic delivery dates will reduce customer anxiety, customer service tickets, and chargeback rates.
