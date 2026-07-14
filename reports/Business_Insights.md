# Olist E-Commerce In-Depth Business Insights Report

This report provides detailed operational analyses across Olist's core strategic pillars: Growth, Logistics, Customer Retention, and Payment Conversions.

---

## 1. Growth & Revenue Performance

### Observation
From Jan 2017 (GMV: ~130K BRL) to Aug 2018 (GMV: ~1.0M BRL), monthly billing expanded exponentially. A prominent spike is recorded during Q4 2017: **November sales surged by over 60% MoM**, confirming a massive seasonality effect from Black Friday.

### Business Insight
While transaction velocity is healthy, extreme seasonality spikes expose the platform to fulfillment risk. The rapid influx of orders during Black Friday leads to carrier capacity breaches, resulting in severe delivery delays in the weeks following.

### Action Plan
- Establish peak-season SLAs with secondary logistics carriers to absorb volume spikes.
- Introduce marketing campaigns in October and January to smooth out seasonal volatility.

---

## 2. Customer Cohorts & Lifetime Retention

### Observation
- **First-Month Customer Retention**: Drops below **0.5%** in month 1 across all cohorts.
- **Repeat Purchase Rate (RPR)**: ~3.2%. Over 96% of customer profiles in our database contain only a single transaction.

```
+---------------+---------+---------+---------+---------+
| Cohort Month  | Month 0 | Month 1 | Month 2 | Month 3 |
+---------------+---------+---------+---------+---------+
| Jan 2017      | 100.00% |   0.39% |   0.18% |   0.39% |
| Feb 2017      | 100.00% |   0.23% |   0.29% |   0.11% |
| Mar 2017      | 100.00% |   0.49% |   0.34% |   0.38% |
+---------------+---------+---------+---------+---------+
```

### Business Insight
Olist acts as a *transactional destination* rather than a recurring ecosystem. The high CAC (Customer Acquisition Cost) required to acquire new buyers is not recovered via recurring transactions, which squeezes profit margins.

### Action Plan
- **Post-Purchase Loyalty Trigger**: Automatically email a 10% voucher valid for 30 days once an order is marked as delivered.
- **Subscription Model**: Offer "Olist Prime" to high-value Southeast customers, providing free shipping on Class A products in exchange for an annual subscription fee.

---

## 3. Logistics & Transit Bottlenecks

### Observation
- **Median Delivery Time**: 10.2 days.
- **SLA Breach Rate (Late Deliveries)**: 6.6% platform-wide.
- **Geographic Variance**: Deliveries in São Paulo (SP) take a median of 7 days, whereas deliveries to northern and remote states (like Alagoas, Pará) take a median of 20+ days.
- **Delay Severity**: Once an order misses its estimated delivery date, the average delay is 6.4 days.

### Business Insight
Logistics bottlenecks are the single largest source of customer friction: **nearly 37% of 1 and 2-star reviews are explicitly caused by late deliveries.** A late delivery drops the average customer review rating from **4.3** (on-time) down to **2.2** (late).

```
Average Review Rating vs. Delivery Speed:
- On-Time / Early: 4.3 Stars (🟢 Healthy)
- Late Delivery:    2.2 Stars (🔴 Critical)
```

### Action Plan
- **Centralized Warehousing**: Set up fulfillment hubs in the Southeast corridor (SP/RJ/MG) to store Class A inventories, cutting median transit time down to 2 days for major urban hubs.
- **Carrier SLAs**: Audit underperforming carrier companies in remote northern regions and re-allocate delivery volumes to regional private carriers.

---

## 4. Payment Checkout Dynamics

### Observation
- **Payment Method Share**: Credit cards are the preferred checkout choice (73%), followed by Boleto (cash slips, 19%), vouchers, and debit cards.
- **AOV Correlation**: Credit card checkouts yield the highest AOV (~165 BRL). A positive correlation exists between credit card installments and basket size: customers buying with 6+ installments spend substantially more.

### Business Insight
Flexible credit financing is a major lever for ticket growth. Customers use installments to finance higher-ticket purchases (e.g. watches_gifts, electronics), which lifts overall platform GMV.

### Action Plan
- Partner with credit card networks to offer interest-free installments (up to 6 terms) for Class A listings.
- Offer small checkout discounts (e.g. 5%) on Boleto checkouts to incentivize immediate cash settlements.
