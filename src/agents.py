"""
Multi-Agent System for Natural Language to SQL
Implements the architecture from the video:
1. Main Conversational Agent - handles user interaction
2. SQL Generator Agent - specialized in SQL query generation
"""
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from database import DatabaseManager
from schema import SchemaExtractor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import AI libraries
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain_anthropic import ChatAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class SQLAgentSystem:
    """
    Multi-agent system for natural language to SQL conversion
    Mimics the n8n workflow architecture from the video
    """

    def __init__(self, db_path: str, model: str = None):
        self.db_manager = DatabaseManager(db_path)
        self.schema_extractor = SchemaExtractor(db_path)

        # Extract schema and generate context
        self.schema_extractor.extract_schema()
        self.ai_context = self.schema_extractor.generate_ai_context()

        # Initialize AI model
        self.model = model or os.getenv("AI_MODEL", "gpt-4o")
        self.llm = self._init_llm()

        # Agent prompts
        self.main_agent_prompt = self._build_main_agent_prompt()
        self.sql_agent_prompt = self._build_sql_agent_prompt()

    def _init_llm(self):
        """Initialize the language model"""

        if self.model.startswith("gpt"):
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI not available. Run: pip install langchain-openai")

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")

            return ChatOpenAI(
                model=self.model,
                temperature=0,
                api_key=api_key
            )

        elif self.model.startswith("claude"):
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("Anthropic not available. Run: pip install langchain-anthropic")

            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")

            return ChatAnthropic(
                model=self.model,
                temperature=0,
                api_key=api_key
            )

        elif "llama" in self.model or "mixtral" in self.model or "gemma" in self.model:
            if not GROQ_AVAILABLE:
                raise ImportError("Groq not available. Run: pip install langchain-groq")

            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment")

            return ChatGroq(
                model_name=self.model,
                temperature=0,
                api_key=api_key
            )

        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def _build_main_agent_prompt(self) -> str:
        """Build prompt for main conversational agent"""

        return f"""You are a helpful data analyst assistant with access to an e-commerce database.

{self.ai_context}

Your role is to help users understand their data by:
1. Answering questions about the database
2. Generating SQL queries when needed
3. Explaining results in plain English
4. Having natural conversations about the data

RESPONSE FORMAT:
You must respond in valid JSON format with this exact structure:
{{
    "response": "Your natural language response to the user",
    "needs_query": true/false,
    "enhanced_query": "Enhanced version of user question (if needs_query=true)",
    "visualization": {{
        "type": "none|table|bar|line|pie",
        "x_label": "Label for x-axis",
        "y_label": "Label for y-axis",
        "title": "Chart title"
    }}
}}

GUIDELINES:
- Set needs_query=true only when the user asks for data/metrics that require querying
- For greetings, clarifications, or follow-ups, set needs_query=false
- When needs_query=true, enhance the query with specific column names and context
- Choose appropriate visualization type based on the data requested
- Keep responses concise and friendly

EXAMPLE INTERACTIONS:

User: "Hi there!"
Response: {{"response": "Hello! I'm your data analyst assistant. I can help you explore the e-commerce database with 100,000+ orders. What would you like to know?", "needs_query": false, "enhanced_query": null, "visualization": {{"type": "none"}}}}

User: "Show me top selling products"
Response: {{"response": "I'll find the top selling products for you.", "needs_query": true, "enhanced_query": "Get the top 10 products by total quantity sold, including product_id and total units sold from order_items table", "visualization": {{"type": "bar", "x_label": "Product", "y_label": "Units Sold", "title": "Top 10 Selling Products"}}}}

User: "What about monthly revenue?"
Response: {{"response": "I'll calculate the monthly revenue trends.", "needs_query": true, "enhanced_query": "Calculate total revenue (sum of price + freight_value) grouped by month from order_items joined with orders, using order_purchase_timestamp for the date", "visualization": {{"type": "line", "x_label": "Month", "y_label": "Revenue ($)", "title": "Monthly Revenue Trends"}}}}
"""

    def _build_sql_agent_prompt(self) -> str:
        """Build prompt for SQL generator agent"""

        return f"""You are a SQL expert specialized in SQLite query generation.

{self.ai_context}

Your ONLY job is to generate a single, valid SQLite SELECT query based on the user's request.

CRITICAL RULES:
1. Generate ONLY the SQL query - no explanations, no markdown, no extra text
2. Use only SELECT statements (never UPDATE, DELETE, DROP, etc.)
3. Use proper JOINs based on the relationships defined above
4. Include appropriate WHERE clauses to filter data
5. Use GROUP BY for aggregations
6. Add ORDER BY for sorted results
7. Include LIMIT clause (default 10 for lists, 100 for aggregations)
8. Handle NULL values appropriately
9. Use table aliases for readability
10. For dates, use strftime() function

QUERY OPTIMIZATION:
- Only join tables that are needed for the query
- Use indexes when available (primary keys, foreign keys)
- Limit result sets to reasonable sizes

EXAMPLES:

Request: "Get top 10 products by total quantity sold"
Query:
SELECT
    p.product_id,
    COUNT(oi.order_id) as total_orders,
    SUM(oi.order_item_id) as total_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_quantity DESC
LIMIT 10

Request: "Calculate monthly revenue for 2017"
Query:
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) as month,
    ROUND(SUM(oi.price + oi.freight_value), 2) as revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE strftime('%Y', o.order_purchase_timestamp) = '2017'
GROUP BY month
ORDER BY month

Request: "Show payment method distribution"
Query:
SELECT
    payment_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_payments), 2) as percentage
FROM order_payments
GROUP BY payment_type
ORDER BY count DESC

Now generate the SQL query for the following request:
"""

    def process_user_query(
        self,
        user_message: str,
        session_id: str = "default",
        chat_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Process user query through the multi-agent system

        Args:
            user_message: User's natural language question
            session_id: Session identifier for chat history
            chat_history: Optional chat history (will load from DB if not provided)

        Returns:
            Dictionary with response, data, and metadata
        """

        result = {
            "response": "",
            "data": None,
            "visualization": {"type": "none"},
            "metadata": {
                "needs_query": False,
                "sql_query": None,
                "query_success": False,
                "error": None
            }
        }

        try:
            # Step 1: Main agent determines if we need to query database
            main_response = self._call_main_agent(user_message, chat_history)

            result["response"] = main_response["response"]
            result["visualization"] = main_response["visualization"]
            result["metadata"]["needs_query"] = main_response["needs_query"]

            # Save user message to history
            self.db_manager.save_chat_message(session_id, "user", user_message)

            # Step 2: If query needed, call SQL generator
            if main_response["needs_query"] and main_response["enhanced_query"]:
                sql_query = self._call_sql_agent(main_response["enhanced_query"])

                result["metadata"]["sql_query"] = sql_query

                # Step 3: Execute query
                success, data, query_metadata = self.db_manager.execute_query(sql_query)

                result["metadata"]["query_success"] = success
                result["metadata"]["query_metadata"] = query_metadata

                if success:
                    result["data"] = data

                    # Update response with results summary
                    result["response"] += f"\n\nFound {len(data)} results."
                else:
                    error_msg = query_metadata.get("execution", {}).get("error", "Unknown error")
                    result["response"] = f"I encountered an error: {error_msg}"
                    result["metadata"]["error"] = error_msg

            # Save assistant response to history
            self.db_manager.save_chat_message(session_id, "assistant", result["response"])

        except Exception as e:
            result["response"] = f"I encountered an unexpected error: {str(e)}"
            result["metadata"]["error"] = str(e)

        return result

    def _call_main_agent(self, user_message: str, chat_history: Optional[List[Dict]] = None) -> Dict:
        """Call the main conversational agent"""

        messages = []

        # Add system prompt
        messages.append({
            "role": "system",
            "content": self.main_agent_prompt
        })

        # Add chat history if available
        if chat_history:
            messages.extend(chat_history[-5:])  # Last 5 messages for context

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Call LLM
        response = self.llm.invoke(messages)

        # Parse JSON response
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "response": response.content,
                "needs_query": False,
                "enhanced_query": None,
                "visualization": {"type": "none"}
            }

    def _call_sql_agent(self, enhanced_query: str) -> str:
        """Call the SQL generator agent"""

        prompt = self.sql_agent_prompt + "\n\n" + enhanced_query

        messages = [
            {"role": "system", "content": "You are a SQL expert. Generate only valid SQL queries."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm.invoke(messages)

        # Extract SQL query (remove markdown if present)
        sql_query = response.content.strip()

        # Remove markdown code blocks if present
        if sql_query.startswith("```"):
            sql_query = sql_query.split("```")[1]
            if sql_query.startswith("sql"):
                sql_query = sql_query[3:]
            sql_query = sql_query.strip()

        return sql_query


if __name__ == "__main__":
    # Test the agent system
    project_dir = Path(__file__).parent.parent
    db_path = project_dir / "data" / "ecommerce.db"

    if not db_path.exists():
        print("❌ Database not found. Run: python src/setup_database.py")
        exit(1)

    print("🤖 Initializing AI Agent System...\n")

    try:
        agent = SQLAgentSystem(str(db_path))
        print("✅ Agent system initialized\n")

        # Test queries
        test_queries = [
            "Hello!",
            "How many orders are in the database?",
            "Show me the top 5 customer states by number of orders"
        ]

        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"USER: {query}")
            print(f"{'='*60}")

            result = agent.process_user_query(query, session_id="test")

            print(f"\nASSISTANT: {result['response']}")

            if result['metadata']['needs_query']:
                print(f"\nSQL: {result['metadata']['sql_query']}")

            if result['data'] is not None:
                print(f"\nData preview:")
                print(result['data'].head())

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have set up your API keys in .env file")
