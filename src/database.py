"""
Database operations and query execution
"""
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional
from validator import SQLValidator

class DatabaseManager:
    """Manages database connections and query execution"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.validator = SQLValidator()
        self.query_log = []

    def execute_query(self, sql_query: str) -> Tuple[bool, Any, Dict]:
        """
        Execute SQL query with validation

        Returns:
            Tuple of (success, result, metadata)
        """

        # Validate query
        is_valid, cleaned_query, validation_info = self.validator.validate(sql_query)

        metadata = {
            "original_query": sql_query,
            "cleaned_query": cleaned_query,
            "validation": validation_info,
            "execution": {}
        }

        if not is_valid:
            metadata["execution"]["success"] = False
            metadata["execution"]["error"] = "Query validation failed"
            metadata["execution"]["errors"] = validation_info["errors"]
            return False, None, metadata

        # Execute query
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(cleaned_query, conn)
            conn.close()

            metadata["execution"]["success"] = True
            metadata["execution"]["rows_returned"] = len(df)
            metadata["execution"]["columns"] = list(df.columns)

            # Log successful query
            self.query_log.append({
                "query": cleaned_query,
                "rows": len(df),
                "success": True
            })

            return True, df, metadata

        except Exception as e:
            metadata["execution"]["success"] = False
            metadata["execution"]["error"] = str(e)

            # Log failed query
            self.query_log.append({
                "query": cleaned_query,
                "error": str(e),
                "success": False
            })

            return False, None, metadata

    def get_chat_history(self, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        """Retrieve chat history for a session"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT role, content FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))

        history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
        conn.close()

        # Reverse to get chronological order
        return list(reversed(history))

    def save_chat_message(self, session_id: str, role: str, content: str):
        """Save a chat message to history"""

        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO chat_history (session_id, role, content)
            VALUES (?, ?, ?)
        """, (session_id, role, content))
        conn.commit()
        conn.close()

    def clear_chat_history(self, session_id: str):
        """Clear chat history for a session"""

        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

    def get_all_sessions(self) -> List[str]:
        """Get all unique session IDs"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT DISTINCT session_id
            FROM chat_history
            ORDER BY MAX(timestamp) DESC
        """)

        sessions = [row[0] for row in cursor.fetchall()]
        conn.close()

        return sessions

    def get_query_stats(self) -> Dict:
        """Get statistics about executed queries"""

        if not self.query_log:
            return {"total": 0, "successful": 0, "failed": 0}

        total = len(self.query_log)
        successful = sum(1 for q in self.query_log if q["success"])

        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": f"{(successful/total)*100:.1f}%" if total > 0 else "0%"
        }

    def test_connection(self) -> bool:
        """Test database connection"""

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except:
            return False


if __name__ == "__main__":
    # Test database operations
    project_dir = Path(__file__).parent.parent
    db_path = project_dir / "data" / "ecommerce.db"

    if not db_path.exists():
        print("❌ Database not found. Run: python src/setup_database.py")
        exit(1)

    db = DatabaseManager(str(db_path))

    print("🧪 Testing database operations\n")

    # Test connection
    if db.test_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")
        exit(1)

    # Test valid query
    print("\n📊 Testing valid query...")
    success, result, metadata = db.execute_query("""
        SELECT order_status, COUNT(*) as count
        FROM orders
        GROUP BY order_status
        ORDER BY count DESC
    """)

    if success:
        print("✅ Query executed successfully")
        print(f"Rows returned: {len(result)}")
        print("\nResults:")
        print(result)
    else:
        print("❌ Query failed")
        print(f"Error: {metadata['execution'].get('error')}")

    # Test invalid query
    print("\n🚫 Testing invalid query...")
    success, result, metadata = db.execute_query("DROP TABLE orders")

    if not success:
        print("✅ Query correctly blocked")
        print(f"Reason: {metadata['validation']['errors']}")
    else:
        print("❌ Query should have been blocked!")

    # Test chat history
    print("\n💬 Testing chat history...")
    db.save_chat_message("test_session", "user", "Hello")
    db.save_chat_message("test_session", "assistant", "Hi there!")

    history = db.get_chat_history("test_session")
    print(f"✅ Retrieved {len(history)} messages")

    # Get stats
    print("\n📊 Query Statistics:")
    stats = db.get_query_stats()
    print(f"Total queries: {stats['total']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Success rate: {stats['success_rate']}")
