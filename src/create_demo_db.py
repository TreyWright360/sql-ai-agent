"""
Script to generate a small 'Demo' version of Instacart DB for GitHub Deployment
(Full dataset is too large for GitHub free tier)
"""
import sqlite3
import pandas as pd
import zipfile
import os
from pathlib import Path

def create_demo_database():
    print("Creating Demo Database (Small version for Deployment)...")
    
    # Paths
    base_dir = Path(__file__).parent.parent
    zip_path = base_dir / "instacart-market-basket-analysis.zip"
    db_path = base_dir / "data" / "instacart.db"
    
    # Create data dir if not exists
    db_path.parent.mkdir(exist_ok=True)
    
    # Remove existing db to be safe
    if db_path.exists():
        os.remove(db_path)
        
    conn = sqlite3.connect(str(db_path))
    
    # Limit rows for demo (keep it under 50MB)
    DEMO_LIMIT = 15000 
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            # Helper to load and save
            def load_and_save(filename, table_name, limit=None):
                print(f"   Processing {table_name}...")
                # Extract to memory
                with z.open(filename) as f:
                    if filename.endswith('.zip'):
                        # Nested zip support if needed, but likely flat in this specific file structure 
                        # usually kaggle zips are flat or contain folder
                        pass
                
                # Direct read from zip
                # Note: The structure inside the zip might vary. Let's try reading directly.
                # If specific files are inside a folder, we might need to adjust.
                
                # Check file list first
                pass

            # List files
            files = z.namelist()
            print(f"   Found files: {files}")
            
            # Map known files
            file_map = {
                'aisles.csv': 'aisles',
                'departments.csv': 'departments',
                'products.csv': 'products',
                'orders.csv': 'orders',
                'order_products__train.csv': 'order_products__train',
                'order_products__prior.csv': 'order_products__prior'
            }
            
            # Handle potential subdirectories in zip
            actual_files = {}
            for f in files:
                for k in file_map.keys():
                    if f.endswith(k) and '__MACOSX' not in f:
                        actual_files[file_map[k]] = f
                        
            # Load tables
            # 1. Dimensions (Small, load all)
            for table in ['aisles', 'departments', 'products']:
                if table in actual_files:
                    print(f"Loading {table} (full)...")
                    df = pd.read_csv(z.open(actual_files[table]))
                    df.to_sql(table, conn, if_exists='replace', index=False)
            
            # 2. Orders (Limit)
            if 'orders' in actual_files:
                print(f"Loading orders (limit {DEMO_LIMIT})...")
                df_orders = pd.read_csv(z.open(actual_files['orders']), nrows=DEMO_LIMIT)
                df_orders.to_sql('orders', conn, if_exists='replace', index=False)
                
                # Get list of valid order_ids to filter items
                valid_order_ids = set(df_orders['order_id'].unique())
                valid_product_ids = set(pd.read_sql("SELECT product_id FROM products", conn)['product_id'].unique())
             
            # 3. Order Items (Filter by valid orders)
            for table in ['order_products__train', 'order_products__prior']:
                if table in actual_files:
                    print(f"Loading {table} (filtered)...")
                    # Read in chunks to find matching orders
                    chunk_size = 50000
                    chunks = []
                    row_count = 0
                    
                    for chunk in pd.read_csv(z.open(actual_files[table]), chunksize=chunk_size):
                        # Filter for orders we actually have
                        filtered = chunk[chunk['order_id'].isin(valid_order_ids)]
                        
                        # Also filter for products we have (just in case)
                        filtered = filtered[filtered['product_id'].isin(valid_product_ids)]
                        
                        chunks.append(filtered)
                        row_count += len(filtered)
                        if row_count >= DEMO_LIMIT * 5: # Avg 5 items per order
                            break
                    
                    if chunks:
                        df_items = pd.concat(chunks)
                        df_items.to_sql(table, conn, if_exists='replace', index=False)

        # Create Indexes
        print("Creating indexes...")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_aisle ON products(aisle_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_dept ON products(department_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ops_prior_order ON order_products__prior(order_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ops_prior_prod ON order_products__prior(product_id)")
        
        # Create Chat History
        print("Creating chat_history...")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.close()
        
        # Check size
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"\nSUCCESS! Instacart Demo DB created.")
        print(f"Size: {size_mb:.2f} MB")
        
        if size_mb > 95:
            print("WARNING: DB is close to GitHub 100MB limit.")
        else:
            print("DB is safe for GitHub.")
            
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_demo_database()
