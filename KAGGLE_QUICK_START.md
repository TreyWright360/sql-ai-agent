# Kaggle Dataset Quick Start ⚡

**Goal:** Supercharge your SQL Agent with 3.4 Million interactions using the Instacart Dataset.

## 🚀 Setup Steps

### 1. Install Kaggle
```bash
pip install kaggle
```

### 2. Configure API Key
1.  Go to [https://www.kaggle.com/settings](https://www.kaggle.com/settings)
2.  Click **"Create New Token"**.
3.  Save the `kaggle.json` file to:
    *   **Windows**: `C:\Users\YOUR_USER\.kaggle\kaggle.json`
    *   **Mac/Linux**: `~/.kaggle/kaggle.json`

### 3. Download Data
Run this command in the root of your project:
```bash
kaggle datasets download -d psparks/instacart-market-basket-analysis
```

### 4. Run Setup Script
```bash
python examples/instacart/setup_instacart.py
```
*This takes 5-10 minutes. It extracts the raw CSVs and builds an optimized SQLite database.*

### 5. Run Your Agent!
Point your `.env` or application config to use the new database path:
`data/instacart.db`

---

## 🧪 Quick Test Query
Once connected, try this query in your agent to verify:
> "Show me the top 5 most popular products."

If it returns "Bananas", you are live! 🍌
