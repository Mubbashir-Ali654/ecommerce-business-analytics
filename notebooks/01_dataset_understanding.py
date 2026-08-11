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

#print("\nFirst 5 products:")
#print(products.head())

#print("\nShape:")
#print(products.shape)

#print("\nColumns:")
#print(products.columns)

#print("\nData types:")
#print(products.dtypes)

#print("\nMissing values:")
#print(products.isnull().sum())

#print("\nDuplicate rows:")
#print(products.duplicated().sum())
#print("\nUnique product IDs:")
#print(products["product_id"].nunique())

#print(
#    "Unique products in order_items:",
#    order_items["product_id"].nunique()
#)

#print(
#    "Unique products in products:",
#    products["product_id"].nunique()
#)

#missing_products = (
#    set(order_items["product_id"])
#    - set(products["product_id"])
#)

#print(
#    "Product IDs in order_items but missing from products:",
#    len(missing_products)
#)


# ==========================================
# ORDER ITEMS + PRODUCTS
# ==========================================

#items_products = order_items.merge(
#    products[
#        [
#            "product_id",
#            "product_category_name"
#        ]
#    ],
#    on="product_id",
#    how="left"
#)

#print("\nMerged data:")
#print(items_products.head())

#print("\nShape:")
#print(items_products.shape)

#print("\nMissing product categories:")
#print(
#    items_products["product_category_name"].isnull().sum()
#)

#print(
#    "Rows before merge:",
#    len(order_items)
#)

#print(
#    "Rows after merge:",
#    len(items_products)
#)

#category_revenue = (
#    items_products
#    .groupby("product_category_name")["price"]
#    .sum()
#    .sort_values(ascending=False)
#)

#print("\nTop 10 categories by revenue:")
#print(category_revenue.head(10))

#print(
#    "\nNumber of product categories:",
#    category_revenue.shape[0]
#)

#uncategorized_revenue = items_products.loc[
#    items_products["product_category_name"].isna(),
#    "price"
#].sum()

#total_revenue = items_products["price"].sum()

#print("Revenue from uncategorized products:", uncategorized_revenue)

#print(
#    "Uncategorized revenue percentage:",
#    f"{uncategorized_revenue / total_revenue * 100:.2f}%"
#)


#import matplotlib.pyplot as plt
#import seaborn as sns

#top_10_categories = (
#    items_products
#    .dropna(subset=["product_category_name"])
#    .groupby("product_category_name")["price"]
#    .sum()
#    .sort_values(ascending=False)
#    .head(10)
#    .sort_values()
#)

#plt.figure(figsize=(10, 6))

#sns.barplot(
#    x=top_10_categories.values,
#    y=top_10_categories.index
#)

#plt.title("Top 10 Product Categories by Sales Value")
#plt.xlabel("Sales Value")
#plt.ylabel("Product Category")

#plt.tight_layout()

#plt.savefig(
#    "visualizations/top_10_categories_by_revenue.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()


 # ==========================================
# PAYMENTS DATASET
# ==========================================

payments = pd.read_csv(
    "data/olist_order_payments_dataset.csv"
)

#print("\nFirst 5 payments:")
#print(payments.head())

#print("\nShape:")
#print(payments.shape)

#print("\nColumns:")
#print(payments.columns)

#print("\nData types:")
#print(payments.dtypes)

#print("\nMissing values:")
#print(payments.isnull().sum())

#print("\nDuplicate rows:")
#print(payments.duplicated().sum())

#print("\nPayment types:")
#print(payments["payment_type"].value_counts())

#print("\nPayment type percentage:")
#print(
#    payments["payment_type"]
#    .value_counts(normalize=True)
#    .mul(100)
#    .round(2)
#)


#print("\nInstallment statistics:")
#print(payments["payment_installments"].describe())

#print("\nInstallment distribution:")
#print(
#    payments["payment_installments"]
#    .value_counts()
#    .sort_index()
#)

#print("\nPayment value statistics:")
#print(payments["payment_value"].describe())


#payment_counts = (
#    payments
#    .groupby("order_id")
#    .size()
#    .sort_values(ascending=False)
#)

#print("\nTop orders by number of payment records:")
#print(payment_counts.head(10))

#print(
#    "\nOrders with multiple payment records:",
#    (payment_counts > 1).sum()
#)

#print(
#    "Maximum payment records for one order:",
#    payment_counts.max()
#)

#payment_order_ids = set(payments["order_id"])
#order_ids = set(orders["order_id"])

#missing_orders = payment_order_ids - order_ids

#print(
#    "Payment orders missing from orders:",
#    len(missing_orders)
#)

#orders_without_payment = order_ids - payment_order_ids

#print(
#    "Orders without payment records:",
#    len(orders_without_payment)
#)

# ==========================================
# ORDER-LEVEL PAYMENT SUMMARY
# ==========================================

#order_payment_totals = (
#    payments
#    .groupby("order_id", as_index=False)["payment_value"]
#    .sum()
#    .rename(columns={"payment_value": "total_payment"})
#)

#print("\nOrder-level payment summary:")
#print(order_payment_totals.head())

#print("\nShape:")
#print(order_payment_totals.shape)

#print("\nDuplicate order IDs:")
#print(order_payment_totals["order_id"].duplicated().sum())

#print(
#    "\nTotal payment value:",
#    payments["payment_value"].sum()
#)

#print(
#    "Total aggregated payment:",
#    order_payment_totals["total_payment"].sum()
#)

#orders_with_payments = orders.merge(
#    order_payment_totals,
#    on="order_id",
#    how="left"
#)

#print("\nOrders + payments:")
#print(orders_with_payments.head())

#print("\nShape:")
#print(orders_with_payments.shape)

#print("\nOrders without payment after merge:")
#print(
#    orders_with_payments["total_payment"].isnull().sum()
#)


# ==========================================
# PAYMENT ANALYSIS
# ==========================================

#paid_orders = orders_with_payments.dropna(
#    subset=["total_payment"]
#)

#average_order_value = paid_orders["total_payment"].mean()

#print(
#    "Average Order Value:",
#    round(average_order_value, 2)
#)

#print("\nTotal paid orders:")
#print(len(paid_orders))

#print("\nTotal payment value:")
#print(round(paid_orders["total_payment"].sum(), 2))

#print("\nPayment statistics:")
#print(
#    paid_orders["total_payment"].describe()
#)

#payment_type_revenue = (
#    payments
#    .groupby("payment_type")["payment_value"]
#    .sum()
#    .sort_values(ascending=False)
#)

#print("\nPayment value by payment type:")
#print(payment_type_revenue)

#payment_type_revenue_pct = (
#    payment_type_revenue
#    / payment_type_revenue.sum()
#    * 100
#)

#print("\nPayment value percentage:")
#print(
#    payment_type_revenue_pct.round(2)
#)

# ==========================================
# PAYMENT VISUALIZATION
# ==========================================

#import matplotlib.pyplot as plt

#payment_type_revenue = (
#    payments
#    .groupby("payment_type")["payment_value"]
#    .sum()
#    .sort_values(ascending=False)
#)

#plt.figure(figsize=(10, 6))

#payment_type_revenue.plot(kind="bar")

#plt.title("Payment Value by Payment Type")
#plt.xlabel("Payment Type")
#plt.ylabel("Total Payment Value")

#plt.xticks(rotation=0)
#plt.tight_layout()

#plt.savefig(
#    "visualizations/payment_value_by_type.png",
#    dpi=300
#)

#plt.show()

# ==========================================
# ORDER REVIEWS DATASET
# ==========================================

reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")

#print("\nFirst 5 reviews:")
#print(reviews.head())

#print("\nShape:")
#print(reviews.shape)

#print("\nColumns:")
#print(reviews.columns)

#print("\nData types:")
#print(reviews.dtypes)

#print("\nMissing values:")
#print(reviews.isnull().sum())

#print("\nDuplicate rows:")
#print(reviews.duplicated().sum())

#print("\nReview score distribution:")
#print(reviews["review_score"].value_counts().sort_index())

#print("\nReview score percentage:")
#print(
#    reviews["review_score"]
#    .value_counts(normalize=True)
#    .sort_index()
#    .mul(100)
#    .round(2)
#)

#print("\nAverage review score:")
#print(reviews["review_score"].mean())

#print("\nReview score statistics:")
#print(reviews["review_score"].describe())


# ==========================================
# REVIEW QUALITY ANALYSIS
# ==========================================

#print("\nReviews by score:")
#print(reviews["review_score"].value_counts().sort_index())

# Positive / negative review groups
#positive_reviews = reviews[reviews["review_score"] >= 4]
#negative_reviews = reviews[reviews["review_score"] <= 2]

#print("\nPositive reviews (4-5):")
#print(len(positive_reviews))

#print("\nNegative reviews (1-2):")
#print(len(negative_reviews))

#print("\nPositive review percentage:")
#print(round(len(positive_reviews) / len(reviews) * 100, 2))

#print("\nNegative review percentage:")
#print(round(len(negative_reviews) / len(reviews) * 100, 2))

# Reviews with written comments
#reviews_with_comments = reviews[
#    reviews["review_comment_message"].notna()
#]

#print("\nReviews with written comments:")
#print(len(reviews_with_comments))

#print("\nReviews without written comments:")
#print(reviews["review_comment_message"].isna().sum())

#print("\nWritten comment percentage:")
#print(
#    round(
#        len(reviews_with_comments) / len(reviews) * 100,
#        2
#    )
#)

## Check whether every review belongs to a unique order
#print("\nUnique orders with reviews:")
#print(reviews["order_id"].nunique())

#print("\nReviews per order:")
#print(reviews["order_id"].value_counts().head(10))


# ==========================================
# REVIEW SCORE VISUALIZATION
# ==========================================

#import matplotlib.pyplot as plt

#review_counts = reviews["review_score"].value_counts().sort_index()

#plt.figure(figsize=(8, 5))

#plt.bar(
#    review_counts.index.astype(str),
#    review_counts.values
#)

#plt.title("Review Score Distribution")
#plt.xlabel("Review Score")
#plt.ylabel("Number of Reviews")

#plt.tight_layout()

#plt.savefig(
#    "visualizations/review_score_distribution.png",
#    dpi=300,
#    bbox_inches="tight"
#)

#plt.show()


# ==========================================
# SELLERS DATASET
# ==========================================

sellers = pd.read_csv("data/olist_sellers_dataset.csv")

#print("\nFirst 5 sellers:")
#print(sellers.head())

#print("\nShape:")
#print(sellers.shape)

#print("\nColumns:")
#print(sellers.columns)

#print("\nData types:")
#print(sellers.dtypes)

#print("\nMissing values:")
#print(sellers.isnull().sum())

#print("\nDuplicate rows:")
#print(sellers.duplicated().sum())

#print("\nUnique seller IDs:")
#print(sellers["seller_id"].nunique())

#print("\nUnique seller states:")
#print(sellers["seller_state"].nunique())

#print("\nTop seller states:")
#print(sellers["seller_state"].value_counts().head(10))

#print("\nTop seller cities:")
#print(sellers["seller_city"].value_counts().head(10))



# ==========================================
# GEOLOCATION DATASET
# ==========================================

geolocation = pd.read_csv("data/olist_geolocation_dataset.csv")

#print("\nFirst 5 geolocation records:")
#print(geolocation.head())

#print("\nShape:")
#print(geolocation.shape)

#print("\nColumns:")
#print(geolocation.columns)

#print("\nData types:")
#print(geolocation.dtypes)

#print("\nMissing values:")
#print(geolocation.isnull().sum())

#print("\nDuplicate rows:")
#print(geolocation.duplicated().sum())

#print("\nUnique zip code prefixes:")
#print(geolocation["geolocation_zip_code_prefix"].nunique())

#print("\nUnique cities:")
#print(geolocation["geolocation_city"].nunique())

#print("\nUnique states:")
#print(geolocation["geolocation_state"].nunique())

#print("\nTop states:")
#print(geolocation["geolocation_state"].value_counts().head(10))

#print("\nTop cities:")
#print(geolocation["geolocation_city"].value_counts().head(10))


# ==========================================
# PRODUCT CATEGORY TRANSLATION DATASET
# ==========================================

category_translation = pd.read_csv(
    "data/product_category_name_translation.csv"
)

print("\nFirst 5 category translations:")
print(category_translation.head())

print("\nShape:")
print(category_translation.shape)

print("\nColumns:")
print(category_translation.columns)

print("\nData types:")
print(category_translation.dtypes)

print("\nMissing values:")
print(category_translation.isnull().sum())

print("\nDuplicate rows:")
print(category_translation.duplicated().sum())

print("\nUnique Portuguese categories:")
print(category_translation["product_category_name"].nunique())

print("\nUnique English categories:")
print(category_translation["product_category_name_english"].nunique())