"""
Streamlit UI for SQL AI Agent
Beautiful chat interface with auto-visualizations
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
from datetime import datetime
import uuid

from agents import SQLAgentSystem
from database import DatabaseManager

# Page configuration
st.set_page_config(
    page_title="SQL AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .assistant-message {
        background-color: #e8f4f8;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sql-query {
        background-color: #282c34;
        color: #abb2bf;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize Streamlit session state"""

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        # Initialize agent system
        project_dir = Path(__file__).parent.parent
        db_path = project_dir / "data" / "ecommerce.db"

        if not db_path.exists():
            st.error("❌ Database not found! Please run `python src/setup_database.py` first.")
            st.stop()

        try:
            st.session_state.agent = SQLAgentSystem(str(db_path))
            st.session_state.db_manager = DatabaseManager(str(db_path))
        except Exception as e:
            st.error(f"❌ Failed to initialize agent: {e}")
            st.error("Make sure you have set up your API keys in the .env file")
            st.stop()


def create_visualization(df: pd.DataFrame, viz_config: dict):
    """Create visualization based on data and configuration"""

    viz_type = viz_config.get("type", "table")

    if viz_type == "table" or viz_type == "none" or df is None or len(df) == 0:
        return None

    try:
        # Determine x and y columns
        columns = df.columns.tolist()

        if len(columns) < 2:
            return None

        x_col = columns[0]
        y_col = columns[1]

        # Create visualization
        if viz_type == "bar":
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                title=viz_config.get("title", ""),
                labels={x_col: viz_config.get("x_label", x_col),
                       y_col: viz_config.get("y_label", y_col)}
            )
            fig.update_layout(xaxis_tickangle=-45)

        elif viz_type == "line":
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                title=viz_config.get("title", ""),
                labels={x_col: viz_config.get("x_label", x_col),
                       y_col: viz_config.get("y_label", y_col)},
                markers=True
            )

        elif viz_type == "pie":
            fig = px.pie(
                df,
                names=x_col,
                values=y_col,
                title=viz_config.get("title", "")
            )

        else:
            return None

        fig.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        return fig

    except Exception as e:
        st.error(f"Visualization error: {e}")
        return None


def display_sample_queries():
    """Display sample query buttons"""

    st.markdown("### 💡 Try these questions:")

    sample_queries = [
        "How many orders are in the database?",
        "Show me monthly revenue trends for 2017",
        "What are the top 10 product categories by sales?",
        "Show me the payment method distribution",
        "Which states have the highest average delivery time?",
    ]

    cols = st.columns(2)

    for idx, query in enumerate(sample_queries):
        col = cols[idx % 2]
        if col.button(query, key=f"sample_{idx}", use_container_width=True):
            return query

    return None


def main():
    """Main application"""

    init_session_state()

    # Sidebar
    with st.sidebar:
        st.title("🤖 SQL AI Agent")
        st.markdown("---")

        st.markdown("### 📊 Database Info")
        st.info("""
        **Olist E-Commerce**
        - 100,000+ orders
        - 9 interconnected tables
        - 2016-2018 data
        """)

        st.markdown("---")

        # Session management
        st.markdown("### 💬 Sessions")

        sessions = st.session_state.db_manager.get_all_sessions()

        if st.button("➕ New Session", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()

        if sessions and len(sessions) > 1:
            selected_session = st.selectbox(
                "Load previous session:",
                options=["Current"] + sessions[:5],
                index=0
            )

            if selected_session != "Current" and selected_session != st.session_state.session_id:
                st.session_state.session_id = selected_session
                # Load messages
                history = st.session_state.db_manager.get_chat_history(selected_session, limit=50)
                st.session_state.messages = history
                st.rerun()

        st.markdown("---")

        # Stats
        st.markdown("### 📈 Statistics")
        query_stats = st.session_state.db_manager.get_query_stats()

        col1, col2 = st.columns(2)
        col1.metric("Total Queries", query_stats.get("total", 0))
        col2.metric("Success Rate", query_stats.get("success_rate", "0%"))

        st.markdown("---")

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.db_manager.clear_chat_history(st.session_state.session_id)
            st.session_state.messages = []
            st.rerun()

    # Main content
    st.title("💬 Chat with Your Data")

    # Display sample queries if no messages
    if len(st.session_state.messages) == 0:
        st.markdown("""
        Welcome! I'm your AI data analyst. I can help you explore the e-commerce database
        by answering questions in plain English.
        """)

        sample_query = display_sample_queries()

        if sample_query:
            st.session_state.messages.append({"role": "user", "content": sample_query})
            st.rerun()

    # Chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Display data and visualization if available
            if message["role"] == "assistant" and "data" in message:
                if message["data"] is not None and len(message["data"]) > 0:
                    # Show visualization
                    if "visualization" in message and message["visualization"]["type"] != "none":
                        fig = create_visualization(message["data"], message["visualization"])
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)

                    # Show data table in expander
                    with st.expander("📊 View Data", expanded=False):
                        st.dataframe(message["data"], use_container_width=True)

                # Show SQL query in expander
                if "sql_query" in message and message["sql_query"]:
                    with st.expander("🔍 SQL Query", expanded=False):
                        st.code(message["sql_query"], language="sql")

    # Chat input
    if prompt := st.chat_input("Ask a question about your data..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Process query
                result = st.session_state.agent.process_user_query(
                    prompt,
                    session_id=st.session_state.session_id,
                    chat_history=st.session_state.messages[-5:]  # Last 5 messages for context
                )

                # Display response
                st.markdown(result["response"])

                # Store full result in message
                assistant_message = {
                    "role": "assistant",
                    "content": result["response"],
                    "data": result["data"],
                    "visualization": result["visualization"],
                    "sql_query": result["metadata"].get("sql_query")
                }

                # Display visualization
                if result["data"] is not None and len(result["data"]) > 0:
                    if result["visualization"]["type"] != "none":
                        fig = create_visualization(result["data"], result["visualization"])
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)

                    # Show data in expander
                    with st.expander("📊 View Data", expanded=False):
                        st.dataframe(result["data"], use_container_width=True)

                # Show SQL query
                if result["metadata"].get("sql_query"):
                    with st.expander("🔍 SQL Query", expanded=False):
                        st.code(result["metadata"]["sql_query"], language="sql")

                # Add to messages
                st.session_state.messages.append(assistant_message)


if __name__ == "__main__":
    main()
