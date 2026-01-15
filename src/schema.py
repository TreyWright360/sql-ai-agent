"""
Database schema extraction and context generation for AI agents
Similar to the Python script shown in the video
"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any

class SchemaExtractor:
    """Extract database schema and generate AI context"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.schema_info = {}

    def extract_schema(self) -> Dict[str, Any]:
        """Extract complete database schema"""

        # Get all tables
        cursor = self.conn.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'chat_history'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]

        # Detect Dataset Type
        if "aisles" in tables and "departments" in tables:
            self.dataset_type = "instacart"
            db_name = "Instacart Market Basket"
        else:
            self.dataset_type = "olist"
            db_name = "Olist Brazilian E-Commerce"

        schema = {
            "database": db_name,
            "tables": {},
            "relationships": self._get_relationships(tables), # Pass tables to helper
            "total_tables": len(tables)
        }

        # Extract info for each table
        for table in tables:
            schema["tables"][table] = self._get_table_info(table)

        self.schema_info = schema
        return schema

    def _get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed information about a table"""

        # Get columns
        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
        columns = []

        for row in cursor.fetchall():
            col_info = {
                "name": row[1],
                "type": row[2],
                "nullable": not row[3],
                "primary_key": bool(row[5])
            }
            columns.append(col_info)

        # Get row count
        cursor = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]

        # Get sample data
        try:
            cursor = self.conn.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample_data = cursor.fetchall()
        except Exception:
            sample_data = []

        return {
            "columns": columns,
            "row_count": row_count,
            "sample_data": sample_data[:3] if sample_data else []
        }

    def _get_relationships(self, tables: List[str] = None) -> List[Dict[str, str]]:
        """Define table relationships based on Schema"""
        
        if getattr(self, 'dataset_type', 'olist') == 'instacart':
            return [
                {"from": "products", "to": "aisles", "via": "aisle_id", "type": "many-to-one"},
                {"from": "products", "to": "departments", "via": "department_id", "type": "many-to-one"},
                {"from": "order_products__prior", "to": "orders", "via": "order_id", "type": "many-to-one"},
                {"from": "order_products__prior", "to": "products", "via": "product_id", "type": "many-to-one"},
                {"from": "order_products__train", "to": "orders", "via": "order_id", "type": "many-to-one"},
                {"from": "order_products__train", "to": "products", "via": "product_id", "type": "many-to-one"},
                {"from": "orders", "to": "orders", "via": "user_id", "type": "many-to-one (same user)"}
            ]

        # Default to Olist
        return [
            {
                "from": "orders",
                "to": "customers",
                "via": "customer_id",
                "type": "many-to-one"
            },
            {
                "from": "order_items",
                "to": "orders",
                "via": "order_id",
                "type": "many-to-one"
            },
            {
                "from": "order_items",
                "to": "products",
                "via": "product_id",
                "type": "many-to-one"
            },
            {
                "from": "order_items",
                "to": "sellers",
                "via": "seller_id",
                "type": "many-to-one"
            },
            {
                "from": "order_payments",
                "to": "orders",
                "via": "order_id",
                "type": "many-to-one"
            },
            {
                "from": "order_reviews",
                "to": "orders",
                "via": "order_id",
                "type": "many-to-one"
            },
            {
                "from": "customers",
                "to": "geolocation",
                "via": "customer_zip_code_prefix = geolocation_zip_code_prefix",
                "type": "many-to-one"
            },
            {
                "from": "sellers",
                "to": "geolocation",
                "via": "seller_zip_code_prefix = geolocation_zip_code_prefix",
                "type": "many-to-one"
            },
            {
                "from": "products",
                "to": "product_category_translation",
                "via": "product_category_name",
                "type": "many-to-one"
            }
        ]

    def generate_ai_context(self) -> str:
        """
        Generate comprehensive context for AI agents
        """

        if not self.schema_info:
            self.extract_schema()
            
        dataset_type = getattr(self, 'dataset_type', 'olist')

        if dataset_type == 'instacart':
            context = f"""# INSTACART MARKET BASKET DATABASE
    
    ## OVERVIEW
    You are analyzing the Instacart Market Basket dataset containing {self.schema_info['total_tables']} tables.
    This contains over 3 million grocery orders, linking users to products, aisles, and departments.
    
    ## TABLES AND COLUMNS
    
    """
        else:
            context = f"""# OLIST BRAZILIAN E-COMMERCE DATABASE

    ## OVERVIEW
    You are analyzing a Brazilian e-commerce dataset containing {self.schema_info['total_tables']} interconnected tables.
    This is real production-like data with {self.schema_info['tables'].get('orders', {}).get('row_count', 'N/A'):,} orders from 2016-2018.

    ## TABLES AND COLUMNS

    """

        # Add detailed table information
        for table_name, table_info in self.schema_info["tables"].items():
            context += f"### {table_name.upper()} ({table_info['row_count']:,} rows)\n"

            for col in table_info["columns"]:
                pk_marker = " [PRIMARY KEY]" if col["primary_key"] else ""
                null_marker = " [NULLABLE]" if col["nullable"] else ""
                context += f"- **{col['name']}** ({col['type']}){pk_marker}{null_marker}\n"

            context += "\n"

        # Add relationships
        context += "## TABLE RELATIONSHIPS\n\n"
        for rel in self.schema_info["relationships"]:
            context += f"- {rel['from']}.{rel['via']} → {rel['to']} ({rel['type']})\n"

        # Add business rules
        if dataset_type == 'instacart':
             context += """
    
    ## CRITICAL BUSINESS RULES (Instacart):
    
    1. **Order Structure**:
       - 'orders' table contains the meta-info (user_id, order_dow, order_hour_of_day).
       - Actual items are in 'order_products__prior' (past orders) and 'order_products__train' (latest order).
       - To get products for an order, JOIN 'orders' -> 'order_products__prior' -> 'products'.
    
    2. **Reorders**:
       - 'reordered' column in order_products indicates if the user has bought this product before (1=Yes, 0=No).
    
    3. **Product Hierarchy**:
       - products -> aisles -> departments.
       - Use this hierarchy for categorization queries (e.g., "Top departments").
    
    4. **Day of Week**:
       - 'order_dow': 0=Sunday, 6=Saturday (typically).
    
    """
        else:
            context += """
    
    ## CRITICAL BUSINESS RULES (Olist):
    
    1. **Date Handling**:
       - Use date columns from 'orders' table for time-based queries
       - Key dates: order_purchase_timestamp, order_delivered_customer_date
    
    2. **Revenue Calculations**:
       - Revenue = SUM(price + freight_value) from order_items
       - Join order_items → orders → customers for customer-level revenue
    
    3. **Delivery Time**:
       - Calculate as: JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_purchase_timestamp)
       - Filter out NULL delivery dates for accurate metrics
    
    4. **Product Categories**:
       - Join products → product_category_translation for English category names
       - product_category_name is in Portuguese, use translation table
    
    5. **Location Data**:
       - Use customer_state or seller_state for state-level analysis
       - Join with geolocation on zip_code_prefix for coordinates
    
    6. **Payment Methods**:
       - Multiple payments possible per order (installments)
       - Use payment_type column for method distribution
    """

        context += """
    ## SQL QUERY GUIDELINES
    
    1. Always use table aliases for readability
    2. Include LIMIT clauses for large result sets
    3. Use proper JOINs based on relationships above
    4. Handle NULL values appropriately (especially dates)
    5. Use aggregate functions (SUM, AVG, COUNT) for metrics
    6. For SQLite, use strftime() for date manipulation
    """

        return context

    def get_table_names(self) -> List[str]:
        """Get list of all table names"""
        if not self.schema_info:
            self.extract_schema()
        return list(self.schema_info["tables"].keys())

    def save_schema(self, output_path: str):
        """Save schema to JSON file"""
        if not self.schema_info:
            self.extract_schema()

        with open(output_path, 'w') as f:
            json.dump(self.schema_info, f, indent=2)

        print(f"✅ Schema saved to: {output_path}")

    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Test schema extraction
    project_dir = Path(__file__).parent.parent
    db_path = project_dir / "data" / "ecommerce.db"

    if not db_path.exists():
        print("❌ Database not found. Run: python src/setup_database.py")
        exit(1)

    extractor = SchemaExtractor(str(db_path))

    print("🔍 Extracting schema...")
    schema = extractor.extract_schema()

    print(f"\n✅ Found {schema['total_tables']} tables:")
    for table_name, info in schema['tables'].items():
        print(f"  - {table_name}: {info['row_count']:,} rows, {len(info['columns'])} columns")

    # Save schema
    output_path = project_dir / "data" / "schema.json"
    extractor.save_schema(str(output_path))

    # Generate AI context
    print("\n📝 Generating AI context...")
    context = extractor.generate_ai_context()
    print(f"Generated {len(context)} characters of context")

    extractor.close()
