import pandas as pd
import numpy as np

customers = pd.read_csv("data/olist_customers_dataset.csv")

#print("First 5 rows:")
#print(customers.head())

#print("\nLast 5 rows:")
#print(customers.tail())

#print("\nShape:")
#print(customers.shape)

#print("\nColumns:")
#print(customers.columns)

#print("\nData types:")
#print(customers.dtypes)

#print("\nDataset info:")
#print(customers.info())

#print("\nStatistical summary:")
#print(customers.describe())

#print("\nUnique values:")
#print(customers.nunique())

#print("\nMissing values:")
#print(customers.isnull().sum())

#print("Duplicate rows:", customers.duplicated().sum())


#unique_counts = customers["customer_unique_id"].value_counts()

#print(unique_counts.head(10))

#print(
#    "Customers appearing more than once:",
#    (unique_counts > 1).sum()
#)


#print(
#    "Maximum records for one customer:",
#    unique_counts.max()
#)


#print(
#    customers["customer_state"]
#    .value_counts()
#    .head(10)
#)


#print(
#    customers["customer_city"]
#    .value_counts()
#    .head(10)
#)

#customer_frequency = (
#    customers
#    .groupby("customer_unique_id")["customer_id"]
#    .count()
#    .sort_values(ascending=False)
#)

#print(customer_frequency.head(10))

#print(
#    customer_frequency.value_counts()
#    .sort_index()
#)


# ==========================================
# ORDERS DATASET
# ==========================================

orders = pd.read_csv("data/olist_orders_dataset.csv")

#print("\nFirst 5 orders:")
#print(orders.head())

#print("\nShape:")
#print(orders.shape)

#print("\nColumns:")
#print(orders.columns)

#print("\nData types:")
#print(orders.dtypes)

#print("\nMissing values:")
#print(orders.isnull().sum())

#print("\nDuplicate rows:")
#print(orders.duplicated().sum())



#print("\nOrder status distribution:")
#print(orders["order_status"].value_counts())

#print("\nSample purchase timestamps:")
#print(orders["order_purchase_timestamp"].head(10))

#print("\nUnique customers in orders:")
#print(orders["customer_id"].nunique())

#print("\nOrders per customer:")
#print(orders["customer_id"].value_counts().head(10))


#status_percentage = (
#    orders["order_status"]
#    .value_counts(normalize=True) * 100
#)

#print(status_percentage.round(2))


#date_columns = [
#    "order_purchase_timestamp",
#    "order_approved_at",
#    "order_delivered_carrier_date",
#    "order_delivered_customer_date",
#    "order_estimated_delivery_date"
#]

#for col in date_columns:
#    orders[col] = pd.to_datetime(orders[col])

#print(orders[date_columns].dtypes)


#print("Earliest order:")
#print(orders["order_purchase_timestamp"].min())

#print("\nLatest order:")
#print(orders["order_purchase_timestamp"].max())

#orders["delivery_days"] = (
#    orders["order_delivered_customer_date"]
#    - orders["order_purchase_timestamp"]
#).dt.total_seconds() / (24 * 60 * 60)

#print(orders["delivery_days"].describe())

#orders["delivery_delay_days"] = (
#    orders["order_delivered_customer_date"]
#    - orders["order_estimated_delivery_date"]
#).dt.total_seconds() / (24 * 60 * 60)


#print("\nDelivery time:")
#print(orders["delivery_days"].describe())

#print("\nDelivery delay:")
#print(orders["delivery_delay_days"].describe())

#print(
#    "\nOrders delivered late:",
#    (orders["delivery_delay_days"] > 0).sum()
#)

#print(
#    "Orders delivered early:",
#    (orders["delivery_delay_days"] < 0).sum()
#)

#print(
#    "Orders delivered exactly on estimate:",
#    (orders["delivery_delay_days"] == 0).sum()
#)

#longest_deliveries = (
#    orders[
#        orders["delivery_days"].notna()
#    ]
#    .sort_values("delivery_days", ascending=False)
#    .loc[
#        :,
#        [
#            "order_id",
#            "order_status",
#            "order_purchase_timestamp",
#            "order_delivered_customer_date",
#            "order_estimated_delivery_date",
#            "delivery_days",
#            "delivery_delay_days"
#        ]
#    ]
#    .head(10)
#)

#print(longest_deliveries)

#late_rate = (
#    (orders["delivery_delay_days"] > 0).sum()
#    / orders["delivery_delay_days"].notna().sum()
#    * 100
#)

#print(f"Late delivery rate: {late_rate:.2f}%")

#print(
#    "Orders delivered in more than 30 days:",
#    (orders["delivery_days"] > 30).sum()
#)

#print(
#    "Orders delivered in more than 60 days:",
#    (orders["delivery_days"] > 60).sum()
#)

#print(
#    "Orders delivered in more than 90 days:",
#    (orders["delivery_days"] > 90).sum()
#)

#delivered_count = orders["delivery_days"].notna().sum()

#print(
#    f">30 days: {(orders['delivery_days'] > 30).sum() / delivered_count * 100:.2f}%"
#)

#print(
#    f">60 days: {(orders['delivery_days'] > 60).sum() / delivered_count * 100:.2f}%"
#)

#print(
#    f">90 days: {(orders['delivery_days'] > 90).sum() / delivered_count * 100:.2f}%"
#)

#print("Mean:", orders["delivery_days"].mean())
#print("Median:", orders["delivery_days"].median())

#print(
#    "90th percentile:",
#    orders["delivery_days"].quantile(0.90)
#)

#print(
#    "95th percentile:",
#    orders["delivery_days"].quantile(0.95)
#)

#print(
#    "99th percentile:",
#    orders["delivery_days"].quantile(0.99)
#)


#orders_with_customer = orders.merge(
#    customers[
#        ["customer_id", "customer_unique_id"]
#    ],
#    on="customer_id",
#    how="left"
#)

#print(orders_with_customer.head())

#print("\nShape:")
#print(orders_with_customer.shape)

#print("\nMissing customer identities:")
#print(
#    orders_with_customer["customer_unique_id"].isnull().sum()
#)


#orders_per_customer = (
#    orders_with_customer
#    .groupby("customer_unique_id")["order_id"]
#    .count()
#    .sort_values(ascending=False)
#)

#print(orders_per_customer.head(10))


#repeat_customers = (
#    orders_per_customer > 1
#).sum()

#total_customers = orders_per_customer.shape[0]

#print("Total customers:", total_customers)
#print("Repeat customers:", repeat_customers)

#repeat_purchase_rate = (
#    repeat_customers / total_customers
#) * 100

#print(
#    f"Repeat purchase rate: {repeat_purchase_rate:.2f}%"
#)

#repeat_distribution = (
#    orders_per_customer[orders_per_customer > 1]
#    .value_counts()
#    .sort_index()
#)

#print(repeat_distribution)

# ==========================================
# ORDER ITEMS DATASET
# ==========================================

order_items = pd.read_csv(
    "data/olist_order_items_dataset.csv"
)

#print("\nFirst 5 order items:")
#print(order_items.head())

#print("\nShape:")
#print(order_items.shape)

#print("\nColumns:")
#print(order_items.columns)

#print("\nData types:")
#print(order_items.dtypes)

#print("\nMissing values:")
#print(order_items.isnull().sum())

#print("\nDuplicate rows:")
#print(order_items.duplicated().sum())

#items_per_order = (
#    order_items
#    .groupby("order_id")["order_item_id"]
#    .count()
#    .sort_values(ascending=False)
#)

#print(items_per_order.head(10))

#print(
#    "Maximum items in one order:",
#    items_per_order.max()
#)

#print("\nPrice statistics:")
#print(order_items["price"].describe())

#print("\nFreight statistics:")
#print(order_items["freight_value"].describe())

#order_items["shipping_limit_date"] = pd.to_datetime(
#    order_items["shipping_limit_date"]
#)

#print(order_items["shipping_limit_date"].dtype)

#print("\nShipping limit date range:")

#print(
#    "Earliest:",
#    order_items["shipping_limit_date"].min()
#)

#print(
#    "Latest:",
#    order_items["shipping_limit_date"].max()
#)


# ==========================================
# PRODUCTS DATASET
# ==========================================

products = pd.read_csv(
    "data/olist_products_dataset.csv"
)

print("\nFirst 5 products:")
print(products.head())

print("\nShape:")
print(products.shape)

print("\nColumns:")
print(products.columns)

print("\nData types:")
print(products.dtypes)

print("\nMissing values:")
print(products.isnull().sum())

print("\nDuplicate rows:")
print(products.duplicated().sum())
print("\nUnique product IDs:")
print(products["product_id"].nunique())

print(
    "Unique products in order_items:",
    order_items["product_id"].nunique()
)

print(
    "Unique products in products:",
    products["product_id"].nunique()
)

missing_products = (
    set(order_items["product_id"])
    - set(products["product_id"])
)

print(
    "Product IDs in order_items but missing from products:",
    len(missing_products)
)


# ==========================================
# ORDER ITEMS + PRODUCTS
# ==========================================

items_products = order_items.merge(
    products[
        [
            "product_id",
            "product_category_name"
        ]
    ],
    on="product_id",
    how="left"
)

print("\nMerged data:")
print(items_products.head())

print("\nShape:")
print(items_products.shape)

print("\nMissing product categories:")
print(
    items_products["product_category_name"].isnull().sum()
)

print(
    "Rows before merge:",
    len(order_items)
)

print(
    "Rows after merge:",
    len(items_products)
)

category_revenue = (
    items_products
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 categories by revenue:")
print(category_revenue.head(10))

print(
    "\nNumber of product categories:",
    category_revenue.shape[0]
)

uncategorized_revenue = items_products.loc[
    items_products["product_category_name"].isna(),
    "price"
].sum()

total_revenue = items_products["price"].sum()

print("Revenue from uncategorized products:", uncategorized_revenue)

print(
    "Uncategorized revenue percentage:",
    f"{uncategorized_revenue / total_revenue * 100:.2f}%"
)


import matplotlib.pyplot as plt
import seaborn as sns

top_10_categories = (
    items_products
    .dropna(subset=["product_category_name"])
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=top_10_categories.values,
    y=top_10_categories.index
)

plt.title("Top 10 Product Categories by Sales Value")
plt.xlabel("Sales Value")
plt.ylabel("Product Category")

plt.tight_layout()

plt.savefig(
    "visualizations/top_10_categories_by_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()