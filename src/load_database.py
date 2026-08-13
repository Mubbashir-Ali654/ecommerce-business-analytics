import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

DB_PATH = DATABASE_DIR / "ecommerce.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


# ============================================================
# SOURCE DATASETS
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
# DATABASE CREATION
# ============================================================

def create_database():
    """Create a fresh SQLite database using the project schema."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_PATH}"
        )

    if DB_PATH.exists():
        DB_PATH.unlink()

    connection = sqlite3.connect(DB_PATH)

    print("Creating database...")

    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)

    print("Database schema created successfully.")

    return connection


# ============================================================
# LOAD CSV DATA
# ============================================================

def load_data(connection):
    """Load all CSV datasets into the corresponding database tables."""

    for table_name, file_name in DATA_FILES.items():

        file_path = DATA_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        print(f"\nLoading {file_name}...")

        dataframe = pd.read_csv(file_path)

        dataframe.to_sql(
            table_name,
            connection,
            if_exists="append",
            index=False,
        )

        print(
            f"Loaded {len(dataframe):,} rows "
            f"into '{table_name}'."
        )


# ============================================================
# DATABASE VERIFICATION
# ============================================================

def verify_database(connection):
    """Verify row counts for every database table."""

    print("\n" + "=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)

    for table_name in DATA_FILES:

        row_count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        print(
            f"{table_name:<25} "
            f"{row_count:>10,} rows"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    connection = create_database()

    try:
        load_data(connection)
        connection.commit()

        verify_database(connection)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    print("\n" + "=" * 60)
    print("Database creation completed successfully.")
    print(f"Database: {DB_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()