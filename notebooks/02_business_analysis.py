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

print("\nOrder items + products:")
print(order_items_products.head())

print("\nShape:")
print(order_items_products.shape)


# Add English category names
order_items_products = order_items_products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

print("\nAfter category translation:")
print(order_items_products.head())


# ==========================================
# CALCULATE REVENUE
# ==========================================

category_revenue = (
    order_items_products
    .groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 categories by revenue:")
print(category_revenue.head(10))


# ==========================================
# TOP 10 REVENUE
# ==========================================

top_10_categories = category_revenue.head(10)

print("\nTop 10 categories:")
print(top_10_categories)


# ==========================================
# VISUALIZATION
# ==========================================

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
    "visualizations/top_10_categories_by_revenue_v2.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()