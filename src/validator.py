"""
SQL Query Validator - Security layer to prevent destructive operations
Critical component from the video to prevent data loss
"""
import re
from typing import Tuple, Dict

class SQLValidator:
    """Validates SQL queries to ensure they're safe to execute"""

    # Destructive keywords that should never appear
    DESTRUCTIVE_KEYWORDS = [
        'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE',
        'INSERT', 'UPDATE', 'REPLACE', 'GRANT', 'REVOKE'
    ]

    # Allowed keywords (read-only operations)
    ALLOWED_KEYWORDS = [
        'SELECT', 'WITH', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT',
        'INNER', 'OUTER', 'ON', 'GROUP', 'BY', 'HAVING', 'ORDER',
        'LIMIT', 'OFFSET', 'AS', 'DISTINCT', 'UNION', 'INTERSECT',
        'EXCEPT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END'
    ]

    def __init__(self):
        self.validation_log = []

    def validate(self, sql_query: str) -> Tuple[bool, str, Dict]:
        """
        Validate SQL query for safety

        Returns:
            Tuple of (is_valid, cleaned_query, validation_info)
        """

        validation_info = {
            "original_query": sql_query,
            "is_valid": False,
            "errors": [],
            "warnings": [],
            "cleaned_query": ""
        }

        # Strip whitespace and comments
        cleaned = self._clean_query(sql_query)

        if not cleaned:
            validation_info["errors"].append("Empty query after cleaning")
            return False, "", validation_info

        # Check for destructive keywords
        destructive_found = self._check_destructive_keywords(cleaned)
        if destructive_found:
            validation_info["errors"].append(
                f"Destructive keywords found: {', '.join(destructive_found)}"
            )
            return False, "", validation_info

        # Check for semicolons (multiple statements)
        if self._contains_multiple_statements(cleaned):
            validation_info["warnings"].append("Multiple statements detected - only first will execute")
            cleaned = cleaned.split(';')[0].strip()

        # Verify it starts with SELECT or WITH
        if not self._starts_with_select(cleaned):
            validation_info["errors"].append("Query must start with SELECT or WITH")
            return False, "", validation_info

        # Check for common SQL injection patterns
        injection_risk = self._check_injection_patterns(cleaned)
        if injection_risk:
            validation_info["warnings"].append(f"Potential injection pattern: {injection_risk}")

        # All checks passed
        validation_info["is_valid"] = True
        validation_info["cleaned_query"] = cleaned

        # Log validation
        self.validation_log.append(validation_info)

        return True, cleaned, validation_info

    def _clean_query(self, query: str) -> str:
        """Remove comments and extra whitespace"""

        # Remove single-line comments
        query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)

        # Remove multi-line comments
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)

        # Normalize whitespace
        query = ' '.join(query.split())

        return query.strip()

    def _check_destructive_keywords(self, query: str) -> list:
        """Check for destructive SQL keywords"""

        query_upper = query.upper()
        found = []

        for keyword in self.DESTRUCTIVE_KEYWORDS:
            # Use word boundaries to avoid false positives
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, query_upper):
                found.append(keyword)

        return found

    def _contains_multiple_statements(self, query: str) -> bool:
        """Check if query contains multiple statements"""
        return ';' in query

    def _starts_with_select(self, query: str) -> bool:
        """Verify query starts with SELECT or WITH"""
        query_upper = query.upper().strip()
        return query_upper.startswith('SELECT') or query_upper.startswith('WITH')

    def _check_injection_patterns(self, query: str) -> str:
        """Check for common SQL injection patterns"""

        patterns = {
            "Union-based": r"UNION\s+SELECT",
            "Comment-based": r"--\s*$|/\*|\*/",
            "Hex-encoded": r"0x[0-9A-Fa-f]+",
            "Stacked queries": r";\s*SELECT|;\s*DROP|;\s*DELETE"
        }

        query_upper = query.upper()

        for pattern_name, pattern in patterns.items():
            if re.search(pattern, query_upper):
                return pattern_name

        return None

    def get_validation_stats(self) -> Dict:
        """Get statistics about validation history"""

        if not self.validation_log:
            return {"total": 0, "valid": 0, "invalid": 0}

        total = len(self.validation_log)
        valid = sum(1 for v in self.validation_log if v["is_valid"])

        return {
            "total": total,
            "valid": valid,
            "invalid": total - valid,
            "success_rate": f"{(valid/total)*100:.1f}%"
        }


def test_validator():
    """Test the validator with various queries"""

    validator = SQLValidator()

    test_queries = [
        # Valid queries
        ("SELECT * FROM orders LIMIT 10", True),
        ("SELECT COUNT(*) FROM customers WHERE customer_state = 'SP'", True),
        ("""
            WITH monthly_revenue AS (
                SELECT strftime('%Y-%m', order_purchase_timestamp) as month,
                       SUM(payment_value) as revenue
                FROM orders o
                JOIN order_payments op ON o.order_id = op.order_id
                GROUP BY month
            )
            SELECT * FROM monthly_revenue
        """, True),

        # Invalid queries
        ("DROP TABLE orders", False),
        ("DELETE FROM customers WHERE customer_id = '123'", False),
        ("UPDATE orders SET order_status = 'delivered'", False),
        ("SELECT * FROM orders; DROP TABLE orders;", False),
        ("INSERT INTO customers VALUES ('test')", False),
    ]

    print("🔒 Testing SQL Validator\n")
    print("="*60)

    for query, should_be_valid in test_queries:
        is_valid, cleaned, info = validator.validate(query)

        status = "✅ PASS" if is_valid == should_be_valid else "❌ FAIL"
        query_preview = query[:50].replace('\n', ' ') + "..." if len(query) > 50 else query

        print(f"\n{status}")
        print(f"Query: {query_preview}")
        print(f"Expected: {'VALID' if should_be_valid else 'INVALID'}")
        print(f"Got: {'VALID' if is_valid else 'INVALID'}")

        if info["errors"]:
            print(f"Errors: {', '.join(info['errors'])}")
        if info["warnings"]:
            print(f"Warnings: {', '.join(info['warnings'])}")

    print("\n" + "="*60)
    stats = validator.get_validation_stats()
    print(f"\n📊 Validation Stats: {stats}")


if __name__ == "__main__":
    test_validator()
