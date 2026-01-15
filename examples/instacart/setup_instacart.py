import os
import zipfile
import pandas as pd
import sqlite3
import glob

# Configuration
DATA_DIR = os.path.join("..", "..", "data", "instacart")
DB_PATH = os.path.join("..", "..", "data", "instacart.db")
ZIP_FILE = "instacart-market-basket-analysis.zip"

def setup_instacart():
    print("Starting Instacart Dataset Setup...")

    # 1. Check if Zip exists (User needs to download it first)
    zip_path = os.path.join("..", "..", ZIP_FILE)
    if not os.path.exists(zip_path):
        # Checks if it was downloaded into the current folder by mistake
        if os.path.exists(ZIP_FILE):
             zip_path = ZIP_FILE
        else:
            print(f"Error: {ZIP_FILE} not found!")
            print("   Please run: kaggle datasets download -d psparks/instacart-market-basket-analysis")
            return

    # 2. Extract Data
    if not os.path.exists(DATA_DIR):
        print(f"Extracting {zip_path} to {DATA_DIR}...")
        os.makedirs(DATA_DIR, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
    else:
        print(f"Data directory found at {DATA_DIR}")

    # 3. Create SQLite Database
    print(f"Creating SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    
    # 4. Load CSVs into SQLite
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    
    for csv_file in csv_files:
        table_name = os.path.basename(csv_file).replace(".csv", "")
        print(f"   PLEASE WAIT: Loading {table_name}...")
        
        # Iterative loading for large files (like order_products)
        chunksize = 100000
        for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunksize)):
            chunk.to_sql(table_name, conn, if_exists="append" if i > 0 else "replace", index=False)
            if i == 0:
                print(f"     -> Created table {table_name}")
        print(f"     -> Finished loading {table_name}")

    # 5. Create Indexes (Crucial for performance)
    print("Optimizing database with indexes...")
    indexes = [
        ("orders", "order_id"),
        ("orders", "user_id"),
        ("order_products__prior", "order_id"),
        ("order_products__prior", "product_id"),
        ("order_products__train", "order_id"),
        ("order_products__train", "product_id"),
        ("products", "product_id"),
        ("products", "aisle_id"),
        ("products", "department_id")
    ]
    
    cursor = conn.cursor()
    for table, col in indexes:
        try:
            print(f"   -> Indexing {table}.{col}...")
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{table}_{col} ON {table}({col})")
        except Exception as e:
            print(f"   Could not index {table}: {e}")
            
    conn.commit()
    conn.close()

    print("\nSUCCESS! Database ready at data/instacart.db")
    print("   You can now run the SQL Agent on this database.")

if __name__ == "__main__":
    setup_instacart()
