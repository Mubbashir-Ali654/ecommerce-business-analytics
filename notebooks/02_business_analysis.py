import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATA
# ============================================================

orders = pd.read_csv("data/olist_orders_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")
payments = pd.read_csv("data/olist_order_payments_dataset.csv")
reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
customers = pd.read_csv("data/olist_customers_dataset.csv")
category_translation = pd.read_csv(
    "data/product_category_name_translation.csv"
)


# ============================================================
# 2. PRODUCT CATEGORY REVENUE ANALYSIS
# ============================================================

order_items_products = order_items.merge(
    products[
        [
            "product_id",
            "product_category_name"
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

category_revenue = (
    order_items_products
    .groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
)

top_10_categories = category_revenue.head(10)

print("\nTop 10 Categories by Revenue:")
print(top_10_categories)


plt.figure(figsize=(10, 6))

plt.barh(
    top_10_categories.index[::-1],
    top_10_categories.values[::-1]
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product Category")

plt.tight_layout()

plt.savefig(
    "visualizations/top_10_categories_by_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# ============================================================
# 3. MONTHLY ORDERS AND REVENUE
# ============================================================

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

orders["month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
)

monthly_orders = (
    orders.groupby("month")["order_id"]
    .nunique()
)

order_payments = (
    payments.groupby("order_id")["payment_value"]
    .sum()
    .reset_index()
)

orders_revenue = orders.merge(
    order_payments,
    on="order_id",
    how="left"
)

monthly_revenue = (
    orders_revenue
    .groupby("month")["payment_value"]
    .sum()
)

monthly_summary = pd.DataFrame({
    "orders": monthly_orders,
    "revenue": monthly_revenue
})

print("\nMonthly Business Summary:")
print(monthly_summary)


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

plt.tight_layout()

plt.savefig(
    "visualizations/monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# ============================================================
# 4. SELLER PERFORMANCE ANALYSIS
# ============================================================

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

seller_performance = pd.DataFrame({
    "revenue": seller_revenue,
    "orders": seller_orders
}).dropna()

print("\nTop 10 Sellers by Revenue:")
print(
    seller_performance
    .sort_values("revenue", ascending=False)
    .head(10)
)

print("\nTop 10 Sellers by Number of Orders:")
print(seller_orders.head(10))


# Top sellers by revenue

top_10_sellers_revenue = (
    seller_revenue
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_sellers_revenue.index,
    top_10_sellers_revenue.values
)

plt.title("Top 10 Sellers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Seller ID")

plt.tight_layout()

plt.savefig(
    "visualizations/top_10_sellers_by_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# Top sellers by order count

top_10_sellers_orders = (
    seller_orders
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_sellers_orders.index,
    top_10_sellers_orders.values
)

plt.title("Top 10 Sellers by Number of Orders")
plt.xlabel("Number of Orders")
plt.ylabel("Seller ID")

plt.tight_layout()

plt.savefig(
    "visualizations/top_10_sellers_by_orders.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# Seller revenue vs order volume

plt.figure(figsize=(10, 6))

plt.scatter(
    seller_performance["orders"],
    seller_performance["revenue"],
    alpha=0.5
)

plt.title("Seller Revenue vs Order Volume")
plt.xlabel("Number of Orders")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    "visualizations/seller_revenue_vs_order_volume.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# ============================================================
# 5. DELIVERY PERFORMANCE
# ============================================================

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"]
)

orders["order_estimated_delivery_date"] = pd.to_datetime(
    orders["order_estimated_delivery_date"]
)

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)

orders["delivery_difference_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / (24 * 60 * 60)

orders["is_late"] = (
    orders["delivery_difference_days"] > 0
)

delivered_orders = orders[
    orders["order_delivered_customer_date"].notna()
].copy()

print("\nAverage Delivery Time:")
print(
    round(delivered_orders["delivery_days"].mean(), 2),
    "days"
)

print("\nMedian Delivery Time:")
print(
    round(delivered_orders["delivery_days"].median(), 2),
    "days"
)

print("\nLate Orders:")
print(
    delivered_orders["is_late"].value_counts()
)

late_delivery_percentage = (
    delivered_orders["is_late"].mean() * 100
)

print(
    "\nLate Delivery Percentage:",
    round(late_delivery_percentage, 2),
    "%"
)


# Monthly delivery performance

delivered_orders["delivery_month"] = (
    delivered_orders["order_purchase_timestamp"]
    .dt.to_period("M")
)

monthly_delivery = (
    delivered_orders
    .groupby("delivery_month")
    .agg(
        total_orders=("order_id", "count"),
        late_orders=("is_late", "sum")
    )
)

monthly_delivery["late_delivery_percentage"] = (
    monthly_delivery["late_orders"]
    / monthly_delivery["total_orders"]
    * 100
)

print("\nMonthly Delivery Performance:")
print(monthly_delivery)


plt.figure(figsize=(12, 6))

plt.plot(
    monthly_delivery.index.astype(str),
    monthly_delivery["late_delivery_percentage"],
    marker="o"
)

plt.title("Monthly Late Delivery Rate")
plt.xlabel("Month")
plt.ylabel("Late Delivery %")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "visualizations/monthly_late_delivery_rate.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# ============================================================
# 6. CUSTOMER REVENUE AND ORDER ANALYSIS
# ============================================================

orders_customers = orders.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id"
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

customer_revenue = (
    orders_customers
    .groupby("customer_unique_id")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

customer_orders = (
    orders_customers
    .groupby("customer_unique_id")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nTop 10 Customers by Revenue:")
print(customer_revenue.head(10))

print("\nTop 10 Customers by Number of Orders:")
print(customer_orders.head(10))


total_revenue = order_payments["payment_value"].sum()

total_orders = orders["order_id"].nunique()

average_order_value = (
    total_revenue / total_orders
)

print("\nTotal Revenue:")
print(round(total_revenue, 2))

print("\nTotal Orders:")
print(total_orders)

print("\nAverage Order Value:")
print(round(average_order_value, 2))


# ============================================================
# 7. ORDER STATUS ANALYSIS
# ============================================================

order_status = (
    orders["order_status"]
    .value_counts()
)

order_status_percentage = (
    orders["order_status"]
    .value_counts(normalize=True)
    * 100
)

print("\nOrder Status:")
print(order_status)

print("\nOrder Status Percentage:")
print(order_status_percentage.round(2))


# ============================================================
# 8. PAYMENT METHOD ANALYSIS
# ============================================================

payments_orders = payments.merge(
    orders[
        [
            "order_id"
        ]
    ],
    on="order_id",
    how="inner"
)

orders_by_payment_method = (
    payments_orders
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

average_order_value_by_payment_method = (
    payments
    .groupby("payment_type")["payment_value"]
    .mean()
    .sort_values(ascending=False)
)

print("\nOrders by Payment Method:")
print(orders_by_payment_method)

print("\nRevenue by Payment Method:")
print(revenue_by_payment_method)

print("\nAverage Order Value by Payment Method:")
print(average_order_value_by_payment_method)


# ============================================================
# 9. CUSTOMER RETENTION / REPEAT CUSTOMERS
# ============================================================

customer_order_counts = (
    orders_customers
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

customer_type = pd.Series(
    "One-time Customer",
    index=customer_order_counts.index
)

customer_type[
    customer_order_counts > 1
] = "Repeat Customer"

customer_type_counts = customer_type.value_counts()

customer_type_percentage = (
    customer_type.value_counts(normalize=True)
    * 100
)

repeat_customers = (
    customer_order_counts[
        customer_order_counts > 1
    ]
)

repeat_customer_percentage = (
    len(repeat_customers)
    / len(customer_order_counts)
    * 100
)

print("\nCustomer Type:")
print(customer_type_counts)

print("\nCustomer Type Percentage:")
print(customer_type_percentage.round(2))

print(
    "\nRepeat Customer Percentage:",
    round(repeat_customer_percentage, 2),
    "%"
)

print("\nTotal Unique Customers:")
print(len(customer_order_counts))

print("\nRepeat Customers:")
print(len(repeat_customers))

print("\nTop Repeat Customers by Number of Orders:")
print(
    repeat_customers
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 10. REVIEW ANALYSIS
# ============================================================

review_score_distribution = (
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

review_score_percentage = (
    reviews["review_score"]
    .value_counts(normalize=True)
    .sort_index()
    * 100
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
    reviews["review_comment_message"].notna()
    & (reviews["review_comment_message"].str.strip() != "")
]

print("\nReview Score Distribution:")
print(review_score_distribution)

print("\nReview Score Percentage:")
print(review_score_percentage.round(2))

print("\nAverage Review Score:")
print(round(average_review_score, 2))

print("\nPositive Reviews (4-5):")
print(len(positive_reviews))

print("\nNegative Reviews (1-2):")
print(len(negative_reviews))

print("\nWritten Reviews:")
print(len(written_reviews))


# ============================================================
# END OF BUSINESS ANALYSIS
# ============================================================

print("\n========================================")
print("BUSINESS ANALYSIS COMPLETED SUCCESSFULLY")
print("========================================")



# ============================================================
# CUSTOMER RETENTION ANALYSIS
# ============================================================

# Count unique orders per customer
customer_order_counts = (
    orders_customers
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)
# Customer type
customer_type = pd.Series(
    "One-time Customer",
    index=customer_order_counts.index
)

customer_type[customer_order_counts > 1] = "Repeat Customer"

customer_type_counts = customer_type.value_counts()

print("\nCustomer Type:")
print(customer_type_counts)

print("\nCustomer Type Percentage:")
print(
    (customer_type_counts / customer_type_counts.sum() * 100)
    .round(2)
)

# Repeat customer rate
repeat_customer_rate = (
    (customer_order_counts > 1).sum()
    / customer_order_counts.count()
    * 100
)

print("\nTotal unique customers:")
print(customer_order_counts.count())

print("\nRepeat customers:")
print((customer_order_counts > 1).sum())

print("\nRepeat customer rate:")
print(round(repeat_customer_rate, 2), "%")

# Top repeat customers
top_repeat_customers = (
    customer_order_counts[customer_order_counts > 1]
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop Repeat Customers:")
print(top_repeat_customers)

# ============================================================
# VISUALIZATION - CUSTOMER TYPE
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    customer_type_counts.index,
    customer_type_counts.values
)

plt.title("Customer Type Distribution")
plt.xlabel("Customer Type")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig(
    "visualizations/customer_type_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()

# ============================================================
# VISUALIZATION - TOP REPEAT CUSTOMERS
# ============================================================

top_repeat_customers_plot = top_repeat_customers.sort_values()

plt.figure(figsize=(10, 6))

plt.barh(
    top_repeat_customers_plot.index,
    top_repeat_customers_plot.values
)

plt.title("Top 10 Repeat Customers by Number of Orders")
plt.xlabel("Number of Orders")
plt.ylabel("Customer ID")

plt.tight_layout()

plt.savefig(
    "visualizations/top_10_repeat_customers.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# ============================================================
# CUSTOMER REVENUE ANALYSIS
# ============================================================

customer_revenue = (
    orders_customers
    .groupby("customer_unique_id")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Customers by Revenue:")
print(customer_revenue.head(10))

print("\nTotal Customer Revenue:")
print(round(customer_revenue.sum(), 2))

print("\nAverage Customer Revenue:")
print(round(customer_revenue.mean(), 2))

print("\nMedian Customer Revenue:")
print(round(customer_revenue.median(), 2))


# ============================================================
# TOP 10 CUSTOMER REVENUE VISUALIZATION
# ============================================================

top_10_customers_revenue = (
    customer_revenue
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_10_customers_revenue.index,
    top_10_customers_revenue.values
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Customer ID")

plt.tight_layout()

plt.savefig(
    "visualizations/top_10_customers_by_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# ============================================================
# CUSTOMER VALUE: ONE-TIME VS REPEAT CUSTOMERS
# ============================================================

customer_summary = pd.DataFrame({
    "orders": customer_order_counts,
    "revenue": customer_revenue
})

customer_summary["customer_type"] = "One-time Customer"

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
        average_revenue=("revenue", "mean")
    )
)

print("\nCustomer Value by Customer Type:")
print(customer_value_by_type)

print("\nAverage Revenue per Customer by Type:")
print(
    customer_value_by_type["average_revenue"].round(2)
)

# ============================================================
# VISUALIZATION
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    customer_value_by_type.index,
    customer_value_by_type["average_revenue"]
)

plt.title("Average Revenue per Customer: One-time vs Repeat")
plt.xlabel("Customer Type")
plt.ylabel("Average Revenue")

plt.tight_layout()

plt.savefig(
    "visualizations/customer_value_by_type.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()


# ============================================================
# DELIVERY PERFORMANCE VS CUSTOMER SATISFACTION
# ============================================================

reviews = pd.read_csv(
    "data/olist_order_reviews_dataset.csv"
)

# Select required review columns
reviews_analysis = reviews[
    [
        "order_id",
        "review_score"
    ]
].copy()

# Merge reviews with delivery information
delivery_reviews = orders[
    [
        "order_id",
        "is_late",
        "delivery_days"
    ]
].merge(
    reviews_analysis,
    on="order_id",
    how="inner"
)

print("\nDelivery + Reviews:")
print(delivery_reviews.head())

print("\nShape:")
print(delivery_reviews.shape)

# Average review score by delivery status
review_by_delivery = (
    delivery_reviews
    .groupby("is_late")["review_score"]
    .agg(["count", "mean"])
)

print("\nReview Score by Delivery Status:")
print(review_by_delivery)

# Review score distribution by delivery status
review_distribution = pd.crosstab(
    delivery_reviews["review_score"],
    delivery_reviews["is_late"],
    normalize="columns"
) * 100

print("\nReview Score Distribution by Delivery Status (%):")
print(review_distribution.round(2))

# ============================================================
# VISUALIZATION
# ============================================================

average_review = (
    delivery_reviews
    .groupby("is_late")["review_score"]
    .mean()
)

average_review.index = [
    "On-time",
    "Late"
]

plt.figure(figsize=(8, 6))

plt.bar(
    average_review.index,
    average_review.values
)

plt.title("Average Review Score: On-time vs Late Delivery")
plt.xlabel("Delivery Status")
plt.ylabel("Average Review Score")

plt.ylim(0, 5)

plt.tight_layout()

plt.savefig(
    "visualizations/review_score_by_delivery_status.png",
    dpi=300,
    bbox_inches="tight"
)

#plt.show()