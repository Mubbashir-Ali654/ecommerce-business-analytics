import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# LOAD DATA
# ==========================================

orders = pd.read_csv("data/olist_orders_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")
category_translation = pd.read_csv(
    "data/product_category_name_translation.csv"
)


# ==========================================
# CATEGORY REVENUE ANALYSIS
# ==========================================

# Connect order items with products
#order_items_products = order_items.merge(
#    products[
#        [
#            "product_id",
#            "product_category_name"
#        ]
#    ],
#    on="product_id",
#    how="left"
#)

#print("\nOrder items + products:")
#print(order_items_products.head())

#print("\nShape:")
#print(order_items_products.shape)


# Add English category names
#order_items_products = order_items_products.merge(
#    category_translation,
#    on="product_category_name",
#    how="left"
#)

#print("\nAfter category translation:")
#print(order_items_products.head())


# ==========================================
# CALCULATE REVENUE
# ==========================================

#category_revenue = (
#    order_items_products
#    .groupby("product_category_name_english")["price"]
#    .sum()
#    .sort_values(ascending=False)
#)

#print("\nTop 10 categories by revenue:")
#print(category_revenue.head(10))


# ==========================================
# TOP 10 REVENUE
# ==========================================

#top_10_categories = category_revenue.head(10)

#print("\nTop 10 categories:")
#print(top_10_categories)


# ==========================================
# VISUALIZATION
# ==========================================

#plt.figure(figsize=(10, 6))

#plt.barh(
#    top_10_categories.index[::-1],
#    top_10_categories.values[::-1]
#)

#plt.title("Top 10 Product Categories by Revenue")
#plt.xlabel("Revenue")
#plt.ylabel("Product Category")

#plt.tight_layout()

#plt.savefig(
#    "visualizations/top_10_categories_by_revenue_v2.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()



# ==========================================
# MONTHLY REVENUE & ORDER TREND
# ==========================================

# Convert purchase timestamp to datetime
#orders["order_purchase_timestamp"] = pd.to_datetime(
#    orders["order_purchase_timestamp"]
#)

# Create month column
#orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M")

# Monthly order count
#monthly_orders = (
#    orders.groupby("month")["order_id"]
#    .nunique()
#)

#print("\nMonthly orders:")
#print(monthly_orders)


# ==========================================
# MERGE ORDERS WITH PAYMENT DATA
# ==========================================

#payments = pd.read_csv(
#    "data/olist_order_payments_dataset.csv"
#)

# Aggregate payments at order level
#order_payments = (
#    payments.groupby("order_id")["payment_value"]
#    .sum()
#    .reset_index()
#)

# Merge payment totals with orders
#orders_revenue = orders.merge(
#    order_payments,
#    on="order_id",
#    how="left"
#)

# Monthly revenue
#monthly_revenue = (
#    orders_revenue
#    .groupby("month")["payment_value"]
#    .sum()
#)

#print("\nMonthly revenue:")
#print(monthly_revenue)


# ==========================================
# MONTHLY SUMMARY
# ==========================================

#monthly_summary = pd.DataFrame({
#    "orders": monthly_orders,
#    "revenue": monthly_revenue
#})

#print("\nMonthly business summary:")
#print(monthly_summary)


# ==========================================
# VISUALIZATION - MONTHLY REVENUE
# ==========================================

#plt.figure(figsize=(12, 6))

#plt.plot(
#    monthly_summary.index.astype(str),
#    monthly_summary["revenue"],
#    marker="o"
#)

#plt.title("Monthly Revenue Trend")
#plt.xlabel("Month")
#plt.ylabel("Revenue")

#plt.xticks(rotation=45)

#plt.tight_layout()

#plt.savefig(
#    "visualizations/monthly_revenue_trend.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()

# =========================
# Seller Revenue Analysis
# =========================

#seller_revenue = (
#    order_items
#    .groupby("seller_id")["price"]
#    .sum()
#    .sort_values(ascending=False)
#)

#print("\nTop 10 sellers by revenue:")
#print(seller_revenue.head(10))

import matplotlib.pyplot as plt

#top_10_sellers = seller_revenue.head(10).sort_values()

#plt.figure(figsize=(10, 6))

#plt.barh(
#    top_10_sellers.index,
#    top_10_sellers.values
#)

#plt.title("Top 10 Sellers by Revenue")
#plt.xlabel("Revenue")
#plt.ylabel("Seller ID")

#plt.tight_layout()

#plt.savefig(
#    "visualizations/top_10_sellers_by_revenue.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()

# =========================
# Top Sellers by Order Count
# =========================

#seller_orders = (
#    order_items
#    .groupby("seller_id")["order_id"]
#    .nunique()
#    .sort_values(ascending=False)
#)

#print("\nTop 10 sellers by number of orders:")
#print(seller_orders.head(10))

#top_10_sellers_orders = seller_orders.head(10).sort_values()

#plt.figure(figsize=(10, 6))

#plt.barh(
#    top_10_sellers_orders.index,
#    top_10_sellers_orders.values
#)

#plt.title("Top 10 Sellers by Number of Orders")
#plt.xlabel("Number of Orders")
#plt.ylabel("Seller ID")

#plt.tight_layout()

#plt.savefig(
#    "visualizations/top_10_sellers_by_orders.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()

# =========================
# Seller Revenue vs Order Volume
# =========================

#seller_performance = pd.DataFrame({
#    "revenue": seller_revenue,
#    "orders": seller_orders
#}).dropna()

#print("\nSeller performance:")
#print(seller_performance.sort_values("revenue", ascending=False).head(10))


#plt.figure(figsize=(10, 6))

#plt.scatter(
#    seller_performance["orders"],
#    seller_performance["revenue"],
#    alpha=0.5
#)

#plt.title("Seller Revenue vs Order Volume")
#plt.xlabel("Number of Orders")
#plt.ylabel("Revenue")

#plt.tight_layout()

#plt.savefig(
#    "visualizations/seller_revenue_vs_order_volume.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()

# Convert delivery-related columns to datetime
#orders['order_purchase_timestamp'] = pd.to_datetime(
#    orders['order_purchase_timestamp']
#)

#orders['order_delivered_customer_date'] = pd.to_datetime(
#    orders['order_delivered_customer_date']
#)

#orders['order_estimated_delivery_date'] = pd.to_datetime(
#    orders['order_estimated_delivery_date']
#)

# Calculate actual delivery time in days
#orders['delivery_days'] = (
#    orders['order_delivered_customer_date']
#    - orders['order_purchase_timestamp']
#).dt.total_seconds() / (24 * 60 * 60)

# Calculate difference between actual and estimated delivery
#orders['delivery_difference_days'] = (
#    orders['order_delivered_customer_date']
#    - orders['order_estimated_delivery_date']
#).dt.total_seconds() / (24 * 60 * 60)

# Late delivery flag
#orders['is_late'] = orders['delivery_difference_days'] > 0

#print("Average delivery time:",
#      round(orders['delivery_days'].mean(), 2), "days")

#print("\nMedian delivery time:",
#      round(orders['delivery_days'].median(), 2), "days")

#print("\nLate orders:")
#print(orders['is_late'].value_counts())

#print("\nLate delivery percentage:",
 #     round(orders['is_late'].mean() * 100, 2), "%")

# ==========================================
# LATE DELIVERY ANALYSIS BY MONTH
# ==========================================

# Create month based on order purchase date

#orders['delivery_month'] = (
#    orders['order_purchase_timestamp']
#    .dt.to_period('M')
#)

# Monthly delivery performance

#monthly_delivery = orders.groupby('delivery_month').agg(
#    total_orders=('order_id', 'count'),
#    late_orders=('is_late', 'sum')
#)

# Calculate late delivery percentage

#monthly_delivery['late_delivery_percentage'] = (
#    monthly_delivery['late_orders'] /
#    monthly_delivery['total_orders'] * 100
#)

#print("\nMonthly Delivery Performance:")
#print(monthly_delivery)

# ==========================================
# VISUALIZATION - MONTHLY LATE DELIVERY RATE
# ==========================================

#plt.figure(figsize=(12, 6))

#plt.plot(
#    monthly_delivery.index.astype(str),
#    monthly_delivery['late_delivery_percentage'],
#    marker='o'
#)

#plt.title("Monthly Late Delivery Rate")
#plt.xlabel("Month")
#plt.ylabel("Late Delivery Percentage (%)")

#plt.xticks(rotation=45)

#plt.tight_layout()

#plt.savefig(
#    "visualizations/monthly_late_delivery_rate.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()




# ==========================================
# CUSTOMER ANALYSIS
# ==========================================

#customers = pd.read_csv(
#    "data/olist_customers_dataset.csv"
#)

#payments = pd.read_csv(
#    "data/olist_order_payments_dataset.csv"
#)

# ==========================================
# CUSTOMER REVENUE
# ==========================================

# Total payment per order
#order_payments = (
#    payments.groupby("order_id")["payment_value"]
#    .sum()
#    .reset_index()
#)

# Connect orders with payments
#orders_customers = orders[
#    ["order_id", "customer_id"]
#].merge(
#    order_payments,
#    on="order_id",
#    how="left"
#)

# Customer revenue
#customer_revenue = (
#    orders_customers
#    .groupby("customer_id")["payment_value"]
#    .sum()
#    .sort_values(ascending=False)
#)

#print("\nTop 10 Customers by Revenue:")
#print(customer_revenue.head(10))


# ==========================================
# TOP CUSTOMERS BY ORDER COUNT
# ==========================================

#customer_orders = (
#    orders
#    .groupby("customer_id")["order_id"]
#    .nunique()
#    .sort_values(ascending=False)
#)

#print("\nTop 10 Customers by Number of Orders:")
#print(customer_orders.head(10))


# ==========================================
# AVERAGE ORDER VALUE
# ==========================================

#total_revenue = order_payments["payment_value"].sum()
#total_orders = order_payments["order_id"].nunique()

#average_order_value = total_revenue / total_orders

#print("\nTotal Revenue:", round(total_revenue, 2))
#print("Total Orders:", total_orders)
#print("Average Order Value:", round(average_order_value, 2))


# ==========================================
# CUSTOMER REVENUE VISUALIZATION
# ==========================================

#top_10_customers = (
#    customer_revenue
#    .head(10)
#    .sort_values()
#)

#plt.figure(figsize=(10, 6))

#plt.barh(
#    top_10_customers.index,
#    top_10_customers.values
#)

#plt.title("Top 10 Customers by Revenue")
#plt.xlabel("Revenue")
#plt.ylabel("Customer ID")

#plt.tight_layout()

#plt.savefig(
#    "visualizations/top_10_customers_by_revenue.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()



# ==========================================
# ORDER STATUS ANALYSIS
# ==========================================

#order_status = orders['order_status'].value_counts()

#print("\nOrder Status:")
#print(order_status)

# Order status percentage
#order_status_percentage = (
#    orders['order_status']
#    .value_counts(normalize=True)
#    .mul(100)
#    .round(2)
#)

#print("\nOrder Status Percentage:")
#print(order_status_percentage)

# ==========================================
# VISUALIZATION
# ==========================================

#plt.figure(figsize=(10, 6))

#plt.bar(
#    order_status.index,
#    order_status.values
#)

#plt.title("Order Status Distribution")
#plt.xlabel("Order Status")
#plt.ylabel("Number of Orders")

#plt.xticks(rotation=45)

#plt.tight_layout()

#plt.savefig(
#    "visualizations/order_status_distribution.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()


# ==========================================
# PAYMENT METHOD ANALYSIS
# ==========================================

payments = pd.read_csv(
    "data/olist_order_payments_dataset.csv"
)

# Payment method distribution
payment_orders = (
    payments.groupby("payment_type")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nOrders by Payment Method:")
print(payment_orders)

# Revenue by payment method
payment_revenue = (
    payments.groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Payment Method:")
print(payment_revenue)

# Average Order Value by payment method
payment_aov = (
    payments.groupby("payment_type")["payment_value"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Order Value by Payment Method:")
print(payment_aov)

# ==========================================
# PAYMENT METHOD VISUALIZATION
# ==========================================

plt.figure(figsize=(10, 6))

plt.bar(
    payment_orders.index,
    payment_orders.values
)

plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")

plt.tight_layout()

plt.savefig(
    "visualizations/orders_by_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()