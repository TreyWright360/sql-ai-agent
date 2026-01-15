# Alternative Datasets for Your Portfolio Project

Use these datasets to create your **unique** portfolio project and LinkedIn video. Each dataset is similar in complexity to the Olist dataset but covers different domains.

## 🎯 Best Options for LinkedIn Portfolio Projects

### 1. **Instacart Market Basket Analysis** ⭐ RECOMMENDED
- **Source**: https://www.kaggle.com/c/instacart-market-basket-analysis
- **Size**: 3+ million orders, 200k+ users
- **Tables**: 6 interconnected tables
- **Domain**: Grocery shopping / Retail
- **Why Great**:
  - Very similar structure to Olist
  - Real-world business questions (product recommendations, reorder patterns)
  - Well-documented and popular
  - Great for LinkedIn: "Built AI agent to query 3M+ grocery orders"

**Key Tables**:
- `orders` - Order history
- `products` - Product catalog
- `order_products` - Items in each order
- `aisles` - Product aisles
- `departments` - Store departments

**Sample Questions**:
- "What are the most frequently reordered products?"
- "Show me shopping patterns by day of week"
- "Which departments have the highest cart abandonment?"

---

### 2. **H&M Fashion Recommendations**
- **Source**: https://www.kaggle.com/c/h-and-m-personalized-fashion-recommendations
- **Size**: 30+ million transactions
- **Tables**: 5 tables (transactions, customers, articles, images)
- **Domain**: Fashion / Retail
- **Why Great**:
  - Massive dataset (impressive for portfolio)
  - Modern retail domain
  - Customer segmentation opportunities
  - Great visuals (fashion data)

**Sample Questions**:
- "Show me trending products this season"
- "What's the average purchase frequency by customer age?"
- "Which product categories have the best conversion rates?"

---

### 3. **Rossmann Store Sales**
- **Source**: https://www.kaggle.com/c/rossmann-store-sales
- **Size**: 1M+ sales records, 1,115 stores
- **Tables**: 3 tables (sales, stores, states)
- **Domain**: Retail / Business Analytics
- **Why Great**:
  - Business-focused (great for LinkedIn)
  - Time series data (seasonal trends)
  - Multi-store analysis
  - Simpler than Olist (easier to explain in video)

**Sample Questions**:
- "Compare sales performance across store types"
- "Show me the impact of promotions on revenue"
- "Which stores have the highest customer traffic?"

---

### 4. **Superstore Sales Dataset** ⭐ BEGINNER FRIENDLY
- **Source**: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
- **Size**: ~10k orders (smaller, faster demos)
- **Tables**: 1-3 tables (can be split)
- **Domain**: Office Supplies / Retail
- **Why Great**:
  - Perfect for learning and demos
  - Quick to set up
  - Clean data, less preprocessing
  - Great for "first AI agent" story on LinkedIn

**Sample Questions**:
- "Show me profit by product category"
- "Which regions have the highest sales growth?"
- "Compare shipping modes by delivery time"

---

### 5. **Online Retail II Dataset**
- **Source**: https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci
- **Size**: 500k+ transactions
- **Tables**: 1 main table (can split into 4-5)
- **Domain**: E-commerce / International Sales
- **Why Great**:
  - International sales (multi-country)
  - Real invoices from UK retailer
  - RFM analysis opportunities
  - Good for supply chain insights

**Sample Questions**:
- "What are the top-selling products by country?"
- "Show me customer lifetime value distribution"
- "Which products are frequently bought together?"

---

## 🏢 Enterprise-Level Datasets (Advanced)

### 6. **Northwind Database** (Classic)
- **Source**: Microsoft sample database (available on Kaggle/GitHub)
- **Tables**: 13 tables (suppliers, products, orders, employees, etc.)
- **Domain**: B2B Sales / Supply Chain
- **Why Great**:
  - Industry standard for learning SQL
  - Complex relationships
  - Hiring managers recognize it
  - Free and well-documented

### 7. **Adventure Works Database** (Advanced)
- **Source**: Microsoft sample database
- **Tables**: 70+ tables
- **Domain**: Manufacturing / Sales
- **Why Great**:
  - Enterprise-level complexity
  - Shows you can handle real business systems
  - Great for "scaled to enterprise data" story

---

## 🎓 How to Choose for Your Portfolio

### For Maximum LinkedIn Impact:
1. **Instacart** - "Built AI agent to query 3M+ grocery orders"
2. **H&M** - "Created AI analyst for 30M+ fashion transactions"
3. **Rossmann** - "Developed SQL agent for retail chain analytics"

### For Quick Win / Learning:
1. **Superstore** - Clean, simple, perfect for first project
2. **Online Retail II** - Good middle ground

### For "Wow" Factor:
1. **H&M** - Biggest dataset
2. **Instacart** - Most relatable (everyone shops groceries)

---

## 🚀 How to Use Different Dataset

The system is **dataset-agnostic**! Here's how to swap datasets:

### Step 1: Download your chosen dataset
```bash
# Example for Instacart
cd data/raw
# Download from Kaggle to this folder
```

### Step 2: Modify `setup_database.py`
Update the `table_mappings` dictionary with your CSV filenames:
```python
table_mappings = {
    'orders.csv': 'orders',
    'products.csv': 'products',
    'order_products.csv': 'order_products',
    # ... your tables
}
```

### Step 3: Update relationships in `schema.py`
Modify the `_get_relationships()` method with your table connections.

### Step 4: Run setup
```bash
python src/setup_database.py
```

### Step 5: Test
```bash
streamlit run src/app.py
```

That's it! The AI agents will automatically adapt to your new schema.

---

## 📝 LinkedIn Video Script Template

**Title**: "I Built an AI Agent That Queries [X] Million Rows of [Domain] Data"

**Intro** (10s):
"X months ago, I built an AI agent that can analyze [dataset size] using just natural language..."

**Problem** (20s):
"Writing SQL queries is hard. Business users want insights without learning SQL..."

**Solution** (30s):
"So I built this multi-agent system with: [show features]"

**Demo** (60s):
"Watch this: [ask 3-4 impressive questions, show visualizations]"

**Technical** (30s):
"Under the hood: Python, LangChain, GPT-4, Streamlit, with query validation for security..."

**CTA** (10s):
"Code on GitHub, full tutorial in comments. Follow for more AI projects!"

---

## 💡 Pro Tips

1. **Choose based on your industry**: Retail? Use Instacart. Fashion? Use H&M.

2. **Size matters for LinkedIn**: Bigger numbers = more impressive ("3M orders" > "10k orders")

3. **Tell a story**: "I chose this dataset because I wanted to solve [problem]..."

4. **Show business value**: Focus on insights, not just tech

5. **Make it visual**: Charts and graphs get more engagement than SQL queries

6. **Keep it under 2 minutes**: LinkedIn attention span is short

---

## 🎯 Recommended Choice

**For Codebasics Portfolio**:
→ **Instacart Market Basket Analysis**

**Why**:
- Perfect size (3M orders - impressive but manageable)
- Everyone understands grocery shopping
- Rich business questions
- Similar complexity to video example
- Great for "product manager" or "data analyst" positioning

**Your unique angle**:
"Built AI Agent to Analyze 3 Million Grocery Orders - Ask Questions in Plain English"

This differentiation makes it YOUR project, not a copy of the video.
