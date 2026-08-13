from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VISUALIZATION_DIR = BASE_DIR / "visualizations"

VISUALIZATION_DIR.mkdir(exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_dataset(file_name):
    """Load a CSV dataset from the project data directory."""

    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def save_chart(file_name):
    """Save the current Matplotlib figure."""

    output_path = VISUALIZATION_DIR / file_name

    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 70)
print("LOADING DATA")
print("=" * 70)

orders = load_dataset(
    "olist_orders_dataset.csv"
)

order_items = load_dataset(
    "olist_order_items_dataset.csv"
)

products = load_dataset(
    "olist_products_dataset.csv"
)

payments = load_dataset(
    "olist_order_payments_dataset.csv"
)

reviews = load_dataset(
    "olist_order_reviews_dataset.csv"
)

customers = load_dataset(
    "olist_customers_dataset.csv"
)

sellers = load_dataset(
    "olist_sellers_dataset.csv"
)

category_translation = load_dataset(
    "product_category_name_translation.csv"
)


# ============================================================
# 2. DATE PREPARATION
# ============================================================

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# ============================================================
# 3. ORDER-LEVEL PAYMENT SUMMARY
# ============================================================

order_payments = (
    payments
    .groupby("order_id", as_index=False)["payment_value"]
    .sum()
    .rename(
        columns={
            "payment_value": "order_revenue"
        }
    )
)


# ============================================================
# 4. PRODUCT CATEGORY REVENUE
# ============================================================

print("\n" + "=" * 70)
print("PRODUCT CATEGORY ANALYSIS")
print("=" * 70)

order_items_products = order_items.merge(
    products[
        [
            "product_id",
            "product_category_name",
        ]
    ],
    on="product_id",
    how="left"
)

order_items_products = order_items_products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

order_items_products[
    "product_category_name_english"
] = (
    order_items_products[
        "product_category_name_english"
    ]
    .fillna("Unknown")
)

category_revenue = (
    order_items_products
    .groupby(
        "product_category_name_english"
    )["price"]
    .sum()
    .sort_values(ascending=False)
)

top_10_categories = (
    category_revenue
    .head(10)
    .sort_values()
)

print("\nTop 10 Categories by Revenue:")
print(
    top_10_categories
    .sort_values(ascending=False)
    .round(2)
)


# ============================================================
# VISUALIZATION 1
# ============================================================

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_categories.index,
    top_10_categories.values
)

plt.title(
    "Top 10 Product Categories by Revenue"
)
plt.xlabel("Revenue")
plt.ylabel("Product Category")

save_chart(
    "01_top_10_categories_by_revenue.png"
)


# ============================================================
# 5. MONTHLY ORDERS AND REVENUE
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY BUSINESS PERFORMANCE")
print("=" * 70)

orders["month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
)

orders_with_revenue = orders.merge(
    order_payments,
    on="order_id",
    how="left"
)

monthly_summary = (
    orders_with_revenue
    .groupby("month")
    .agg(
        orders=("order_id", "nunique"),
        revenue=("order_revenue", "sum")
    )
)

print("\nMonthly Business Summary:")
print(
    monthly_summary.round(2)
)


# ============================================================
# VISUALIZATION 2
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_summary.index.astype(str),
    monthly_summary["revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

save_chart(
    "02_monthly_revenue_trend.png"
)


# ============================================================
# 6. SELLER PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("SELLER PERFORMANCE")
print("=" * 70)

seller_revenue = (
    order_items
    .groupby("seller_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

seller_orders = (
    order_items
    .groupby("seller_id")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

seller_performance = pd.concat(
    [
        seller_revenue.rename("revenue"),
        seller_orders.rename("orders"),
    ],
    axis=1
).dropna()

print("\nTop 10 Sellers by Revenue:")
print(
    seller_performance
    .sort_values("revenue", ascending=False)
    .head(10)
    .round(2)
)

print("\nTop 10 Sellers by Order Volume:")
print(
    seller_performance
    .sort_values("orders", ascending=False)
    .head(10)
)


# ============================================================
# VISUALIZATION 3
# ============================================================

top_sellers_revenue = (
    seller_revenue
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_sellers_revenue.index,
    top_sellers_revenue.values
)

plt.title("Top 10 Sellers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Seller ID")

save_chart(
    "03_top_10_sellers_by_revenue.png"
)


# ============================================================
# VISUALIZATION 4
# ============================================================

top_sellers_orders = (
    seller_orders
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_sellers_orders.index,
    top_sellers_orders.values
)

plt.title(
    "Top 10 Sellers by Number of Orders"
)
plt.xlabel("Number of Orders")
plt.ylabel("Seller ID")

save_chart(
    "04_top_10_sellers_by_orders.png"
)


# ============================================================
# VISUALIZATION 5
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    seller_performance["orders"],
    seller_performance["revenue"],
    alpha=0.5
)

plt.title(
    "Seller Revenue vs Order Volume"
)
plt.xlabel("Number of Orders")
plt.ylabel("Revenue")

save_chart(
    "05_seller_revenue_vs_order_volume.png"
)


# ============================================================
# 7. PAYMENT METHOD ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PAYMENT METHOD ANALYSIS")
print("=" * 70)

orders_by_payment_method = (
    payments
    .groupby("payment_type")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

revenue_by_payment_method = (
    payments
    .groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

average_payment_value = (
    payments
    .groupby("payment_type")["payment_value"]
    .mean()
    .sort_values(ascending=False)
)

print("\nOrders by Payment Method:")
print(orders_by_payment_method)

print("\nRevenue by Payment Method:")
print(
    revenue_by_payment_method.round(2)
)

print("\nAverage Payment Value by Method:")
print(
    average_payment_value.round(2)
)


# ============================================================
# VISUALIZATION 6
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    revenue_by_payment_method.index,
    revenue_by_payment_method.values
)

plt.title(
    "Revenue by Payment Method"
)
plt.xlabel("Payment Method")
plt.ylabel("Revenue")

save_chart(
    "06_revenue_by_payment_method.png"
)


# ============================================================
# VISUALIZATION 7
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    orders_by_payment_method.index,
    orders_by_payment_method.values
)

plt.title(
    "Orders by Payment Method"
)
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")

save_chart(
    "07_orders_by_payment_method.png"
)


# ============================================================
# 8. OVERALL BUSINESS METRICS
# ============================================================

total_revenue = (
    order_payments["order_revenue"]
    .sum()
)

total_orders = (
    orders["order_id"]
    .nunique()
)

average_order_value = (
    total_revenue / total_orders
)

print("\n" + "=" * 70)
print("OVERALL BUSINESS METRICS")
print("=" * 70)

print(
    f"\nTotal Revenue: "
    f"R$ {total_revenue:,.2f}"
)

print(
    f"Total Orders: "
    f"{total_orders:,}"
)

print(
    f"Average Order Value: "
    f"R$ {average_order_value:,.2f}"
)


# ============================================================
# 9. ORDER STATUS ANALYSIS
# ============================================================

order_status = (
    orders["order_status"]
    .value_counts()
)

order_status_percentage = (
    orders["order_status"]
    .value_counts(normalize=True)
    .mul(100)
)

print("\n" + "=" * 70)
print("ORDER STATUS ANALYSIS")
print("=" * 70)

print("\nOrder Status:")
print(order_status)

print("\nOrder Status Percentage:")
print(
    order_status_percentage.round(2)
)


# ============================================================
# VISUALIZATION 8
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    order_status.index,
    order_status.values
)

plt.title(
    "Order Status Distribution"
)
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

save_chart(
    "08_order_status_distribution.png"
)


# ============================================================
# 10. CUSTOMER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER ANALYSIS")
print("=" * 70)

orders_customers = orders.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id",
        ]
    ],
    on="customer_id",
    how="left"
)

orders_customers = orders_customers.merge(
    order_payments,
    on="order_id",
    how="left"
)

customer_order_counts = (
    orders_customers
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

customer_revenue = (
    orders_customers
    .groupby("customer_unique_id")[
        "order_revenue"
    ]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Customers by Revenue:")
print(
    customer_revenue
    .head(10)
    .round(2)
)

print("\nTop 10 Customers by Number of Orders:")
print(
    customer_order_counts
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 11. CUSTOMER TYPE / RETENTION
# ============================================================

customer_type = pd.Series(
    "One-time Customer",
    index=customer_order_counts.index
)

customer_type.loc[
    customer_order_counts > 1
] = "Repeat Customer"

customer_type_counts = (
    customer_type
    .value_counts()
)

customer_type_percentage = (
    customer_type
    .value_counts(normalize=True)
    .mul(100)
)

repeat_customers = (
    customer_order_counts[
        customer_order_counts > 1
    ]
)

repeat_customer_rate = (
    len(repeat_customers)
    / len(customer_order_counts)
    * 100
)

print("\n" + "=" * 70)
print("CUSTOMER RETENTION")
print("=" * 70)

print("\nCustomer Type:")
print(customer_type_counts)

print("\nCustomer Type Percentage:")
print(
    customer_type_percentage.round(2)
)

print(
    f"\nTotal Unique Customers: "
    f"{len(customer_order_counts):,}"
)

print(
    f"Repeat Customers: "
    f"{len(repeat_customers):,}"
)

print(
    f"Repeat Customer Rate: "
    f"{repeat_customer_rate:.2f}%"
)


# ============================================================
# VISUALIZATION 9
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    customer_type_counts.index,
    customer_type_counts.values
)

plt.title(
    "Customer Type Distribution"
)
plt.xlabel("Customer Type")
plt.ylabel("Number of Customers")

save_chart(
    "09_customer_type_distribution.png"
)


# ============================================================
# VISUALIZATION 10
# ============================================================

top_repeat_customers = (
    repeat_customers
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_repeat_customers.index,
    top_repeat_customers.values
)

plt.title(
    "Top 10 Repeat Customers by Number of Orders"
)
plt.xlabel("Number of Orders")
plt.ylabel("Customer ID")

save_chart(
    "10_top_10_repeat_customers.png"
)


# ============================================================
# VISUALIZATION 11
# ============================================================

top_customers_revenue = (
    customer_revenue
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_customers_revenue.index,
    top_customers_revenue.values
)

plt.title(
    "Top 10 Customers by Revenue"
)
plt.xlabel("Revenue")
plt.ylabel("Customer ID")

save_chart(
    "11_top_10_customers_by_revenue.png"
)


# ============================================================
# 12. CUSTOMER VALUE ANALYSIS
# ============================================================

customer_summary = pd.DataFrame(
    {
        "orders": customer_order_counts,
        "revenue": customer_revenue,
    }
)

customer_summary["customer_type"] = (
    "One-time Customer"
)

customer_summary.loc[
    customer_summary["orders"] > 1,
    "customer_type"
] = "Repeat Customer"

customer_value_by_type = (
    customer_summary
    .groupby("customer_type")
    .agg(
        customers=("orders", "count"),
        total_revenue=("revenue", "sum"),
        average_revenue=("revenue", "mean"),
    )
)

print("\n" + "=" * 70)
print("CUSTOMER VALUE")
print("=" * 70)

print("\nCustomer Value by Type:")
print(
    customer_value_by_type.round(2)
)

print("\nAverage Revenue per Customer:")
print(
    customer_value_by_type[
        "average_revenue"
    ].round(2)
)


# ============================================================
# VISUALIZATION 12
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    customer_value_by_type.index,
    customer_value_by_type[
        "average_revenue"
    ]
)

plt.title(
    "Average Revenue per Customer: "
    "One-time vs Repeat"
)
plt.xlabel("Customer Type")
plt.ylabel("Average Revenue")

save_chart(
    "12_customer_value_by_type.png"
)


# ============================================================
# 13. DELIVERY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("DELIVERY PERFORMANCE")
print("=" * 70)

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)

orders["delivery_difference_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / (24 * 60 * 60)

delivered_orders = orders[
    orders["order_delivered_customer_date"].notna()
].copy()

delivered_orders["is_late"] = (
    delivered_orders[
        "delivery_difference_days"
    ] > 0
)

average_delivery_time = (
    delivered_orders["delivery_days"]
    .mean()
)

median_delivery_time = (
    delivered_orders["delivery_days"]
    .median()
)

late_delivery_rate = (
    delivered_orders["is_late"]
    .mean()
    * 100
)

print(
    f"\nAverage Delivery Time: "
    f"{average_delivery_time:.2f} days"
)

print(
    f"Median Delivery Time: "
    f"{median_delivery_time:.2f} days"
)

print(
    f"Late Delivery Rate: "
    f"{late_delivery_rate:.2f}%"
)

print(
    f"Late Orders: "
    f"{delivered_orders['is_late'].sum():,}"
)

print(
    f"On-time Orders: "
    f"{(~delivered_orders['is_late']).sum():,}"
)


# ============================================================
# MONTHLY DELIVERY PERFORMANCE
# ============================================================

delivered_orders["delivery_month"] = (
    delivered_orders[
        "order_purchase_timestamp"
    ].dt.to_period("M")
)

monthly_delivery = (
    delivered_orders
    .groupby("delivery_month")
    .agg(
        total_orders=("order_id", "count"),
        late_orders=("is_late", "sum"),
    )
)

monthly_delivery[
    "late_delivery_percentage"
] = (
    monthly_delivery["late_orders"]
    / monthly_delivery["total_orders"]
    * 100
)

print("\nMonthly Delivery Performance:")
print(
    monthly_delivery.round(2)
)


# ============================================================
# VISUALIZATION 13
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_delivery.index.astype(str),
    monthly_delivery[
        "late_delivery_percentage"
    ],
    marker="o"
)

plt.title(
    "Monthly Late Delivery Rate"
)
plt.xlabel("Month")
plt.ylabel("Late Delivery %")

plt.xticks(rotation=45)

save_chart(
    "13_monthly_late_delivery_rate.png"
)


# ============================================================
# 14. DELIVERY PERFORMANCE VS CUSTOMER SATISFACTION
# ============================================================

print("\n" + "=" * 70)
print("DELIVERY VS CUSTOMER SATISFACTION")
print("=" * 70)

reviews_by_order = (
    reviews
    .groupby("order_id")["review_score"]
    .mean()
    .reset_index()
)

delivery_reviews = delivered_orders[
    [
        "order_id",
        "is_late",
        "delivery_days",
    ]
].merge(
    reviews_by_order,
    on="order_id",
    how="inner"
)

review_by_delivery = (
    delivery_reviews
    .groupby("is_late")["review_score"]
    .agg(
        review_count="count",
        average_review_score="mean"
    )
)

print("\nReview Score by Delivery Status:")
print(
    review_by_delivery.round(2)
)

on_time_score = (
    delivery_reviews.loc[
        ~delivery_reviews["is_late"],
        "review_score"
    ].mean()
)

late_score = (
    delivery_reviews.loc[
        delivery_reviews["is_late"],
        "review_score"
    ].mean()
)

print(
    f"\nAverage Review Score - On-time: "
    f"{on_time_score:.2f}"
)

print(
    f"Average Review Score - Late: "
    f"{late_score:.2f}"
)


# ============================================================
# VISUALIZATION 14
# ============================================================

review_comparison = pd.Series(
    {
        "On-time": on_time_score,
        "Late": late_score,
    }
)

plt.figure(figsize=(8, 6))

plt.bar(
    review_comparison.index,
    review_comparison.values
)

plt.title(
    "Average Review Score: "
    "On-time vs Late Delivery"
)
plt.xlabel("Delivery Status")
plt.ylabel("Average Review Score")

plt.ylim(0, 5)

save_chart(
    "14_review_score_by_delivery_status.png"
)


# ============================================================
# 15. REVIEW ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CUSTOMER REVIEW ANALYSIS")
print("=" * 70)

review_score_distribution = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

average_review_score = (
    reviews["review_score"].mean()
)

positive_reviews = reviews[
    reviews["review_score"].isin([4, 5])
]

negative_reviews = reviews[
    reviews["review_score"].isin([1, 2])
]

written_reviews = reviews[
    reviews["review_comment_message"]
    .fillna("")
    .str.strip()
    != ""
]

print("\nReview Score Distribution:")
print(review_score_distribution)

print(
    f"\nAverage Review Score: "
    f"{average_review_score:.2f} / 5"
)

print(
    f"Positive Reviews (4-5): "
    f"{len(positive_reviews):,}"
)

print(
    f"Negative Reviews (1-2): "
    f"{len(negative_reviews):,}"
)

print(
    f"Written Reviews: "
    f"{len(written_reviews):,}"
)


# ============================================================
# VISUALIZATION 15
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    review_score_distribution.index.astype(str),
    review_score_distribution.values
)

plt.title(
    "Review Score Distribution"
)
plt.xlabel("Review Score")
plt.ylabel("Number of Reviews")

save_chart(
    "15_review_score_distribution.png"
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("KEY BUSINESS INSIGHTS")
print("=" * 70)

print(
    f"\n1. The business generated approximately "
    f"R$ {total_revenue:,.2f} in recorded payment value."
)

print(
    f"2. The dataset contains "
    f"{total_orders:,} orders with an "
    f"average order value of "
    f"R$ {average_order_value:,.2f}."
)

print(
    f"3. Repeat customers represent "
    f"{repeat_customer_rate:.2f}% "
    f"of unique customers."
)

print(
    f"4. Average delivery time is "
    f"{average_delivery_time:.2f} days, "
    f"with a late delivery rate of "
    f"{late_delivery_rate:.2f}%."
)

print(
    f"5. Average customer review score is "
    f"{average_review_score:.2f} / 5."
)

print(
    f"6. On-time orders average a review score "
    f"of {on_time_score:.2f}, compared with "
    f"{late_score:.2f} for late orders."
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    f"\nVisualizations generated: "
    f"{len(list(VISUALIZATION_DIR.glob('*.png')))}"
)

print(
    f"Visualization directory: "
    f"{VISUALIZATION_DIR}"
)

print("\nAnalysis complete.")