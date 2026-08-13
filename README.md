# E-Commerce Business Analytics
### Olist Brazilian E-Commerce Dataset — End-to-End Analysis

---

## About This Project

I built this project to apply my data skills on a real-world dataset — moving beyond tutorial exercises into something that resembles actual analytical work.

The dataset comes from Olist, a Brazilian e-commerce platform, and contains roughly 100,000 orders placed between 2016 and 2018. Rather than just running standard EDA, I approached it as a real business problem — identifying revenue drivers, understanding customer behavior, evaluating seller performance, measuring delivery quality, and translating findings into actionable recommendations.

The project combines **Python, Pandas, Matplotlib, SQLite, and SQL** to demonstrate a complete analytical workflow from raw data to business insights.

---

## Analytical Workflow

```
Raw CSV Data
     ↓
Dataset Understanding & Validation
     ↓
Data Cleaning & Transformation
     ↓
Python Business Analysis
     ↓
SQLite Database
     ↓
SQL Business Analysis
     ↓
Visualizations
     ↓
Business Insights & Recommendations
```

---

## Key Metrics

| Metric | Result |
|---|---:|
| Total Revenue | R$ 16,008,872 |
| Total Orders | 99,441 |
| Average Order Value | R$ 160.99 |
| Unique Customers | 96,096 |
| Repeat Customer Rate | 3.12% |
| Average Customer Revenue | R$ 166.59 |
| Average Delivery Time | 12.56 days |
| Late Delivery Rate | 7.87% |

---

## Key Findings

### 1. Customer Retention Is The Biggest Opportunity

Only **3.12% of customers** placed more than one order — yet repeat customers generated nearly **2x the average revenue** of one-time buyers.

| Customer Type | Customers | Average Revenue |
|---|---:|---:|
| One-time | 93,099 | R$ 161.82 |
| Repeat | 2,997 | R$ 314.99 |

With 96,096 unique customers and only 2,997 returning, improving retention is clearly where the biggest untapped revenue opportunity lies.

### 2. Delivery Performance Directly Affects Customer Satisfaction

| Delivery Status | Average Review Score |
|---|---:|
| On-time | 4.21 / 5 |
| Late | 2.57 / 5 |

Late deliveries are not just an operational problem — they are a customer experience problem. A 1.6-point gap in review scores is substantial and directly measurable.

### 3. Credit Cards Dominate Payment Volume

| Payment Method | Revenue | Revenue Share |
|---|---:|---:|
| Credit Card | R$ 12,542,084 | 78.34% |
| Boleto | R$ 2,869,361 | 17.92% |
| Voucher | R$ 379,437 | 2.37% |
| Debit Card | R$ 217,990 | 1.36% |

Credit cards account for 78% of total payment value — making payment reliability a critical operational dependency.

### 4. Revenue Is Unevenly Distributed Across Sellers

Some sellers generate high revenue from fewer orders. Others achieve high revenue through volume. Evaluating sellers on revenue alone gives an incomplete picture — order volume, delivery performance, and review scores all matter.

---

## Business Questions Answered

1. How much revenue does the business generate?
2. What is the Average Order Value?
3. Which product categories generate the most revenue?
4. Which sellers perform best by revenue and by order volume?
5. How does seller revenue relate to order volume?
6. Which payment methods are most commonly used?
7. Which payment methods generate the most revenue?
8. What percentage of customers make repeat purchases?
9. How valuable are repeat customers compared to one-time buyers?
10. What is the average delivery time?
11. What percentage of orders are delivered late?
12. How does late delivery rate vary month to month?
13. Does delivery performance affect customer satisfaction?
14. Where are the biggest business opportunities?

---

## Visualizations

### Monthly Revenue Trend
![Monthly Revenue Trend](visualizations/02_monthly_revenue_trend.png)

### Top 10 Product Categories by Revenue
![Top Categories](visualizations/01_top_10_categories_by_revenue.png)

### Customer Type Distribution
![Customer Type Distribution](visualizations/09_customer_type_distribution.png)

### Customer Value by Type
![Customer Value](visualizations/12_customer_value_by_type.png)

### Review Score by Delivery Status
![Review Score by Delivery](visualizations/14_review_score_by_delivery_status.png)

### Monthly Late Delivery Rate
![Late Delivery Rate](visualizations/13_monthly_late_delivery_rate.png)

### Top 10 Sellers by Revenue
![Top Sellers Revenue](visualizations/03_top_10_sellers_by_revenue.png)

### Revenue by Payment Method
![Payment Revenue](visualizations/06_revenue_by_payment_method.png)

All 15 charts are available in the `visualizations/` directory.

---

## Tech Stack

- **Python** — core analysis language
- **Pandas** — data cleaning, transformation, and aggregation
- **Matplotlib** — business visualizations
- **SQLite** — relational database
- **SQL** — independent query-based analysis and validation
- **Git + GitHub** — version control

---

## Project Structure

```
ecommerce-business-analytics/
│
├── data/                            # Raw Olist CSV datasets (not tracked in Git)
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   └── product_category_name_translation.csv
│
├── database/
│   └── schema.sql                   # Database schema definition
│
├── notebooks/
│   ├── 01_dataset_understanding.py  # Dataset exploration and validation
│   └── 02_business_analysis.py      # Main analysis and visualizations
│
├── sql/
│   └── business_analysis.sql        # 20 SQL queries — independent analysis layer
│
├── src/
│   └── load_database.py             # Creates SQLite database from CSVs
│
├── visualizations/                  # 15 generated PNG charts
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Database

The project includes a relational SQLite database built from the raw CSV datasets.

**Tables:**

| Table | Description |
|---|---|
| customers | Customer records and location data |
| orders | Order lifecycle and timestamps |
| order_items | Individual items within each order |
| order_payments | Payment method and value per order |
| order_reviews | Customer review scores and comments |
| products | Product details and categories |
| sellers | Seller records and location data |
| geolocation | ZIP code to coordinates mapping |
| category_translation | Portuguese to English category names |

The database schema is defined in `database/schema.sql`.
The database is generated locally using `src/load_database.py` and is excluded from Git tracking.

---

## SQL Analysis

The project includes 20 SQL queries covering:

- Overall business performance (revenue, orders, AOV)
- Order status distribution
- Revenue and AOV by payment method
- Monthly revenue trend
- Top product categories by revenue
- Top sellers by revenue and order volume
- Seller revenue vs order volume comparison
- Top customers by revenue
- Customer order frequency and retention
- Customer value by customer type
- Review score distribution
- Delivery performance metrics
- Late delivery rate (overall and monthly)
- Review scores by delivery status
- Positive vs negative review sentiment

SQL queries are available in `sql/business_analysis.sql`.
Results were validated against the Python analysis — key metrics matched exactly.

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Mubbashir-Ali654/ecommerce-business-analytics.git
cd ecommerce-business-analytics
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add the dataset**

Download the Olist dataset from Kaggle and place the CSV files inside `data/`:

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**4. Create the SQLite database**
```bash
python src/load_database.py
```

**5. Run dataset exploration**
```bash
python notebooks/01_dataset_understanding.py
```

**6. Run business analysis**
```bash
python notebooks/02_business_analysis.py
```

Charts are saved automatically to `visualizations/`.

**7. Run SQL analysis**

After creating the database, open `sql/business_analysis.sql` and run the queries against `database/ecommerce.db` using any SQLite client.

---

## Business Recommendations

**1. Prioritize Customer Retention**
With only 3.12% repeat customers, retention is the most significant growth lever available. Repeat customers generate almost twice the average revenue per head — making even small improvements in retention rate meaningful at scale. Post-purchase engagement, loyalty incentives, and personalized follow-ups are worth exploring.

**2. Reduce Late Deliveries**
The 1.6-point gap in review scores between on-time and late orders is one of the clearest findings in the analysis. Late delivery directly damages customer satisfaction. Investigating which sellers, routes, or periods have the highest late delivery rates would be a useful starting point.

**3. Evaluate Sellers on Multiple Dimensions**
Revenue alone does not capture seller quality. A seller KPI framework combining revenue, order volume, delivery performance, and average review score gives a more complete picture of marketplace health — and helps identify sellers who underperform on dimensions that matter to customers.

**4. Monitor Payment Channel Concentration**
Credit cards account for 78% of payment value. Understanding failure rates, fallback options, and customer payment preferences across regions is worth tracking — particularly as the business scales.

---

## What I Learned

**Real data is messier than tutorial data.**
Missing values, inconsistent formats, timestamp parsing, and the need to join across nine related tables — all of these showed up and had to be handled before any analysis could begin. That process is where most of the actual learning happened.

**Python and SQL complement each other.**
Running the same calculations in both and comparing results — for example, total revenue of R$16,008,872 confirmed in both Python and SQL — builds genuine confidence in the analysis. They are not redundant; they validate each other.

**Numbers need context to be useful.**
"3.12% repeat customers" is just a statistic. "3.12% repeat customers who generate almost twice the revenue of one-time buyers" is a business insight. The goal of analytics is the second version, not the first.

---

## Next Steps

This project is designed as version one of an evolving codebase:

- **V2** — Machine learning model to predict late deliveries before they happen
- **V3** — Customer churn prediction using classification algorithms
- **V4** — AI-powered business analyst agent using LLMs and RAG

---

## Dataset

**Olist Brazilian E-Commerce Public Dataset**
Available on Kaggle: [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains approximately 100,000 real orders from the Brazilian e-commerce marketplace between 2016 and 2018, spread across nine related CSV files.

---

## Author

**Mubbashir Ali**
Aspiring AI/LLM Engineer — building practical foundations across data analysis, machine learning, and large language model engineering.

GitHub: [https://github.com/Mubbashir-Ali654](https://github.com/Mubbashir-Ali654)