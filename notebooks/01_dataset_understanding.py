from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ============================================================
# DATA FILES
# ============================================================

DATA_FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


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


def profile_dataset(name, df):
    """Print a concise data-quality profile for a dataset."""

    print("\n" + "=" * 70)
    print(f"{name.upper()} DATASET")
    print("=" * 70)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    print("\nColumns:")
    print(list(df.columns))

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if missing_values.empty:
        print("No missing values.")
    else:
        print(missing_values.sort_values(ascending=False))

    print("\nDuplicate rows:")
    print(df.duplicated().sum())


# ============================================================
# 1. CUSTOMERS
# ============================================================

customers = load_dataset(DATA_FILES["customers"])

profile_dataset("Customers", customers)

print("\nUnique customer IDs:")
print(customers["customer_id"].nunique())

print("\nUnique customer identities:")
print(customers["customer_unique_id"].nunique())

print("\nTop customer states:")
print(
    customers["customer_state"]
    .value_counts()
    .head(10)
)

print("\nTop customer cities:")
print(
    customers["customer_city"]
    .value_counts()
    .head(10)
)

customer_frequency = (
    customers
    .groupby("customer_unique_id")["customer_id"]
    .count()
    .sort_values(ascending=False)
)

print("\nCustomers with multiple customer records:")
print((customer_frequency > 1).sum())

print("\nMaximum records for one customer identity:")
print(customer_frequency.max())


# ============================================================
# 2. ORDERS
# ============================================================

orders = load_dataset(DATA_FILES["orders"])

profile_dataset("Orders", orders)

print("\nOrder status distribution:")
print(
    orders["order_status"]
    .value_counts()
)

order_date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for column in order_date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

print("\nOrder date range:")
print(
    f"Earliest order: "
    f"{orders['order_purchase_timestamp'].min()}"
)

print(
    f"Latest order: "
    f"{orders['order_purchase_timestamp'].max()}"
)

print("\nUnique customers in orders:")
print(orders["customer_id"].nunique())

print("\nOrders per customer:")
print(
    orders["customer_id"]
    .value_counts()
    .head(10)
)

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)

orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / (24 * 60 * 60)

delivered_orders = orders[
    orders["order_delivered_customer_date"].notna()
].copy()

print("\nDelivered orders:")
print(len(delivered_orders))

if not delivered_orders.empty:

    print("\nDelivery time statistics:")
    print(
        delivered_orders["delivery_days"]
        .describe()
        .round(2)
    )

    late_orders = (
        delivered_orders["delivery_delay_days"] > 0
    )

    print("\nLate delivery rate:")
    print(
        f"{late_orders.mean() * 100:.2f}%"
    )

    print("\nOrders delivered late:")
    print(late_orders.sum())

    print("\nOrders delivered early:")
    print(
        (delivered_orders["delivery_delay_days"] < 0).sum()
    )

    print("\nOrders delivered on estimated date:")
    print(
        (delivered_orders["delivery_delay_days"] == 0).sum()
    )


# ============================================================
# 3. ORDER ITEMS
# ============================================================

order_items = load_dataset(DATA_FILES["order_items"])

profile_dataset("Order Items", order_items)

print("\nUnique orders:")
print(order_items["order_id"].nunique())

print("\nUnique products:")
print(order_items["product_id"].nunique())

print("\nUnique sellers:")
print(order_items["seller_id"].nunique())

items_per_order = (
    order_items
    .groupby("order_id")["order_item_id"]
    .count()
    .sort_values(ascending=False)
)

print("\nMaximum items in one order:")
print(items_per_order.max())

print("\nPrice statistics:")
print(
    order_items["price"]
    .describe()
    .round(2)
)

print("\nFreight value statistics:")
print(
    order_items["freight_value"]
    .describe()
    .round(2)
)

order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

print("\nShipping limit date range:")
print(
    f"Earliest: "
    f"{order_items['shipping_limit_date'].min()}"
)

print(
    f"Latest: "
    f"{order_items['shipping_limit_date'].max()}"
)


# ============================================================
# 4. PRODUCTS
# ============================================================

products = load_dataset(DATA_FILES["products"])

profile_dataset("Products", products)

print("\nUnique product IDs:")
print(products["product_id"].nunique())

print("\nNumber of product categories:")
print(
    products["product_category_name"]
    .nunique(dropna=True)
)

print("\nTop product categories:")
print(
    products["product_category_name"]
    .value_counts()
    .head(10)
)

missing_product_ids = (
    set(order_items["product_id"])
    - set(products["product_id"])
)

print(
    "\nProduct IDs in order items but missing "
    "from products:"
)
print(len(missing_product_ids))


# ============================================================
# 5. ORDER ITEMS + PRODUCTS DATA QUALITY CHECK
# ============================================================

order_items_products = order_items.merge(
    products[
        [
            "product_id",
            "product_category_name",
        ]
    ],
    on="product_id",
    how="left",
)

print("\n" + "=" * 70)
print("ORDER ITEMS + PRODUCTS RELATIONSHIP")
print("=" * 70)

print("\nRows before merge:")
print(len(order_items))

print("\nRows after merge:")
print(len(order_items_products))

print("\nMissing product categories after merge:")
print(
    order_items_products["product_category_name"]
    .isnull()
    .sum()
)


# ============================================================
# 6. ORDER PAYMENTS
# ============================================================

payments = load_dataset(DATA_FILES["order_payments"])

profile_dataset("Order Payments", payments)

print("\nPayment type distribution:")
print(
    payments["payment_type"]
    .value_counts()
)

print("\nPayment type percentage:")
print(
    payments["payment_type"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nPayment value statistics:")
print(
    payments["payment_value"]
    .describe()
    .round(2)
)

print("\nInstallment statistics:")
print(
    payments["payment_installments"]
    .describe()
    .round(2)
)

payment_counts = (
    payments
    .groupby("order_id")
    .size()
    .sort_values(ascending=False)
)

print("\nOrders with multiple payment records:")
print((payment_counts > 1).sum())

print("\nMaximum payment records for one order:")
print(payment_counts.max())

payment_order_ids = set(payments["order_id"])
order_ids = set(orders["order_id"])

print("\nPayment records without matching order:")
print(
    len(payment_order_ids - order_ids)
)

print("\nOrders without payment records:")
print(
    len(order_ids - payment_order_ids)
)


# ============================================================
# 7. ORDER REVIEWS
# ============================================================

reviews = load_dataset(DATA_FILES["order_reviews"])

profile_dataset("Order Reviews", reviews)

print("\nReview score distribution:")
print(
    reviews["review_score"]
    .value_counts()
    .sort_index()
)

print("\nReview score percentage:")
print(
    reviews["review_score"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)

print("\nAverage review score:")
print(
    round(
        reviews["review_score"].mean(),
        2
    )
)

positive_reviews = reviews[
    reviews["review_score"] >= 4
]

negative_reviews = reviews[
    reviews["review_score"] <= 2
]

print("\nPositive reviews (4-5):")
print(len(positive_reviews))

print("\nNegative reviews (1-2):")
print(len(negative_reviews))

written_reviews = reviews[
    reviews["review_comment_message"]
    .fillna("")
    .str.strip()
    != ""
]

print("\nReviews with written comments:")
print(len(written_reviews))

print("\nUnique orders with reviews:")
print(reviews["order_id"].nunique())

reviews_per_order = (
    reviews["order_id"]
    .value_counts()
)

print("\nMaximum reviews associated with one order:")
print(reviews_per_order.max())


# ============================================================
# 8. SELLERS
# ============================================================

sellers = load_dataset(DATA_FILES["sellers"])

profile_dataset("Sellers", sellers)

print("\nUnique seller IDs:")
print(sellers["seller_id"].nunique())

print("\nUnique seller states:")
print(sellers["seller_state"].nunique())

print("\nTop seller states:")
print(
    sellers["seller_state"]
    .value_counts()
    .head(10)
)

print("\nTop seller cities:")
print(
    sellers["seller_city"]
    .value_counts()
    .head(10)
)


# ============================================================
# 9. GEOLOCATION
# ============================================================

geolocation = load_dataset(DATA_FILES["geolocation"])

profile_dataset("Geolocation", geolocation)

print("\nUnique zip code prefixes:")
print(
    geolocation["geolocation_zip_code_prefix"]
    .nunique()
)

print("\nUnique cities:")
print(
    geolocation["geolocation_city"]
    .nunique()
)

print("\nUnique states:")
print(
    geolocation["geolocation_state"]
    .nunique()
)

print("\nTop geolocation states:")
print(
    geolocation["geolocation_state"]
    .value_counts()
    .head(10)
)

print("\nTop geolocation cities:")
print(
    geolocation["geolocation_city"]
    .value_counts()
    .head(10)
)


# ============================================================
# 10. CATEGORY TRANSLATION
# ============================================================

category_translation = load_dataset(
    DATA_FILES["category_translation"]
)

profile_dataset(
    "Category Translation",
    category_translation
)

print("\nUnique Portuguese categories:")
print(
    category_translation[
        "product_category_name"
    ].nunique()
)

print("\nUnique English categories:")
print(
    category_translation[
        "product_category_name_english"
    ].nunique()
)


# ============================================================
# 11. CROSS-DATASET RELATIONSHIP CHECKS
# ============================================================

print("\n" + "=" * 70)
print("CROSS-DATASET RELATIONSHIP CHECKS")
print("=" * 70)

customer_ids = set(customers["customer_id"])
order_customer_ids = set(orders["customer_id"])

print("\nOrders with missing customer reference:")
print(
    len(order_customer_ids - customer_ids)
)

product_ids = set(products["product_id"])
item_product_ids = set(order_items["product_id"])

print("\nOrder items with missing product reference:")
print(
    len(item_product_ids - product_ids)
)

seller_ids = set(sellers["seller_id"])
item_seller_ids = set(order_items["seller_id"])

print("\nOrder items with missing seller reference:")
print(
    len(item_seller_ids - seller_ids)
)

review_order_ids = set(reviews["order_id"])

print("\nReviews with missing order reference:")
print(
    len(review_order_ids - order_ids)
)


# ============================================================
# 12. CUSTOMER FREQUENCY ANALYSIS
# ============================================================

customer_orders = (
    orders
    .merge(
        customers[
            [
                "customer_id",
                "customer_unique_id",
            ]
        ],
        on="customer_id",
        how="left",
    )
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

one_time_customers = (
    customer_orders == 1
).sum()

repeat_customers = (
    customer_orders > 1
).sum()

total_unique_customers = (
    customer_orders.count()
)

print("\n" + "=" * 70)
print("CUSTOMER PURCHASE FREQUENCY")
print("=" * 70)

print(
    f"\nTotal unique customers: "
    f"{total_unique_customers:,}"
)

print(
    f"One-time customers: "
    f"{one_time_customers:,}"
)

print(
    f"Repeat customers: "
    f"{repeat_customers:,}"
)

print(
    f"Repeat customer rate: "
    f"{repeat_customers / total_unique_customers * 100:.2f}%"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DATASET UNDERSTANDING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    f"\nDatasets analysed: {len(DATA_FILES)}"
)

print(
    f"Customers: {len(customers):,}"
)

print(
    f"Orders: {len(orders):,}"
)

print(
    f"Order items: {len(order_items):,}"
)

print(
    f"Payments: {len(payments):,}"
)

print(
    f"Reviews: {len(reviews):,}"
)

print(
    f"Products: {len(products):,}"
)

print(
    f"Sellers: {len(sellers):,}"
)

print(
    f"Geolocation records: {len(geolocation):,}"
)

print(
    f"Category translations: "
    f"{len(category_translation):,}"
)

print("\n" + "=" * 70)