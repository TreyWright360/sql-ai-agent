"""
Setup SQLite database from Olist CSV files
Loads all 9 tables with proper relationships
"""
import os
import sys
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

def setup_database():
    """Load CSV files into SQLite database"""

    project_dir = Path(__file__).parent.parent
    raw_dir = project_dir / "data" / "raw"
    db_path = project_dir / "data" / "ecommerce.db"

    # Check if CSV files exist
    if not raw_dir.exists() or not list(raw_dir.glob("*.csv")):
        print("❌ CSV files not found in data/raw/")
        print("\nPlease run: python src/download_dataset.py")
        sys.exit(1)

    print("🗄️  Setting up SQLite database...")
    print(f"📁 Database location: {db_path}\n")

    # Delete existing database
    if db_path.exists():
        print("🗑️  Removing existing database...")
        db_path.unlink()

    # Connect to database
    conn = sqlite3.connect(db_path)

    # Table mapping: CSV filename -> table name
    table_mappings = {
        'olist_customers_dataset.csv': 'customers',
        'olist_geolocation_dataset.csv': 'geolocation',
        'olist_order_items_dataset.csv': 'order_items',
        'olist_order_payments_dataset.csv': 'order_payments',
        'olist_order_reviews_dataset.csv': 'order_reviews',
        'olist_orders_dataset.csv': 'orders',
        'olist_products_dataset.csv': 'products',
        'olist_sellers_dataset.csv': 'sellers',
        'product_category_name_translation.csv': 'product_category_translation'
    }

    total_rows = 0

    for csv_file, table_name in table_mappings.items():
        csv_path = raw_dir / csv_file

        if not csv_path.exists():
            print(f"⚠️  Skipping {csv_file} (not found)")
            continue

        print(f"📊 Loading {table_name}...", end=" ")

        try:
            # Read CSV
            df = pd.read_csv(csv_path)

            # Load into SQLite
            df.to_sql(table_name, conn, if_exists='replace', index=False)

            rows = len(df)
            total_rows += rows
            print(f"✅ {rows:,} rows")

        except Exception as e:
            print(f"❌ Error: {e}")

    # Create indexes for better performance
    print("\n🔗 Creating indexes...")

    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_seller ON order_items(seller_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_payments_order ON order_payments(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_reviews_order ON order_reviews(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_customers_state ON customers(customer_state)",
        "CREATE INDEX IF NOT EXISTS idx_sellers_state ON sellers(seller_state)",
    ]

    for idx_sql in indexes:
        conn.execute(idx_sql)

    conn.commit()

    # Create chat history table
    print("💬 Creating chat history table...")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_history(session_id)")
    conn.commit()

    # Get database stats
    cursor = conn.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = cursor.fetchall()

    conn.close()

    # Print summary
    print("\n" + "="*50)
    print("✅ Database setup complete!")
    print("="*50)
    print(f"📊 Total rows loaded: {total_rows:,}")
    print(f"📁 Tables created: {len(tables)}")
    print(f"\nTables:")
    for (table,) in tables:
        cursor = sqlite3.connect(db_path).execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  - {table}: {count:,} rows")

    print(f"\n✨ Ready to use! Database at: {db_path}")
    print("\n🚀 Next step: Run 'streamlit run src/app.py'")

if __name__ == "__main__":
    setup_database()
