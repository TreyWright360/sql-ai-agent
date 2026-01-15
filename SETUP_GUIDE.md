# Complete Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- API key from OpenAI or Anthropic

---

## 📦 Step 1: Install Dependencies

```bash
cd training/sql-ai-agent

# Install all required packages
pip install -r requirements.txt
```

**What gets installed**:
- Streamlit (UI)
- LangChain (AI framework)
- OpenAI/Anthropic SDKs (AI models)
- SQLAlchemy & Pandas (database)
- Plotly (visualizations)

---

## 🔑 Step 2: Set Up API Keys

### Option A: OpenAI (Recommended for beginners)

1. Get API key: https://platform.openai.com/api-keys
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```bash
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   AI_MODEL=gpt-4o
   ```

**Cost**: ~$0.01-0.05 per query with GPT-4o

### Option B: Anthropic Claude

1. Get API key: https://console.anthropic.com/
2. Edit `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   AI_MODEL=claude-sonnet-4-5
   ```

**Cost**: ~$0.01-0.03 per query with Claude Sonnet

### Model Options:
- `gpt-4o` - Best balance (recommended)
- `gpt-4o-mini` - Cheaper, faster, less accurate
- `claude-sonnet-4-5` - Most accurate
- `claude-opus-4-5` - Premium, very accurate

---

## 💾 Step 3: Download Dataset

### For Olist Dataset (Default):

```bash
# Install Kaggle CLI
pip install kaggle

# Set up Kaggle credentials
# 1. Go to https://www.kaggle.com/settings
# 2. Click "Create New API Token"
# 3. This downloads kaggle.json

mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Download dataset
python src/download_dataset.py
```

### Manual Download (if Kaggle CLI fails):

1. Visit: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Click "Download" (requires free Kaggle account)
3. Extract all CSV files to `data/raw/` folder

### For Alternative Dataset:

See `ALTERNATIVE_DATASETS.md` for other options like Instacart, H&M, etc.

---

## 🗄️ Step 4: Set Up Database

```bash
# This loads all CSV files into SQLite database
python src/setup_database.py
```

**What this does**:
- Creates `ecommerce.db` in `data/` folder
- Loads all 9 tables
- Creates indexes for performance
- Sets up chat history table

**Expected output**:
```
✅ Database setup complete!
📊 Total rows loaded: 112,650
📁 Tables created: 10
```

**Verify it worked**:
```bash
# Should show 10 tables with row counts
sqlite3 data/ecommerce.db "SELECT name FROM sqlite_master WHERE type='table'"
```

---

## 🧪 Step 5: Test Components

### Test 1: Schema Extraction
```bash
python src/schema.py
```

Expected: Shows all tables and generates `data/schema.json`

### Test 2: Query Validator
```bash
python src/validator.py
```

Expected: Shows validation tests passing

### Test 3: Database Operations
```bash
python src/database.py
```

Expected: Executes sample queries

### Test 4: AI Agents (requires API key)
```bash
python src/agents.py
```

Expected: Shows AI responses to test queries

---

## 🚀 Step 6: Launch the App

```bash
streamlit run src/app.py
```

The app should open automatically in your browser at `http://localhost:8501`

---

## 🎯 Using the App

### First Time:

1. You'll see sample questions - click any to try
2. Or type your own question like:
   - "How many orders are there?"
   - "Show me monthly revenue for 2017"
   - "What are the top 10 product categories?"

### Features:

- **Chat Interface**: Ask questions in plain English
- **Auto-Visualization**: Charts appear automatically
- **Data Tables**: Click "View Data" to see raw results
- **SQL Queries**: Click "SQL Query" to see generated SQL
- **Sessions**: Create new sessions or load previous conversations
- **Export**: Copy SQL queries or download data

---

## 🐛 Troubleshooting

### Error: "Database not found"
**Solution**: Run `python src/setup_database.py`

### Error: "OPENAI_API_KEY not found"
**Solution**: Create `.env` file with your API key (see Step 2)

### Error: "No module named 'langchain'"
**Solution**: Run `pip install -r requirements.txt`

### Error: "Kaggle credentials not found"
**Solution**: Follow Step 3 to set up `~/.kaggle/kaggle.json`

### Error: "Query validation failed"
**Solution**: The AI generated a destructive query (UPDATE/DELETE). This is working as intended - the validator blocked it!

### Slow responses
**Solutions**:
- Use `gpt-4o-mini` instead of `gpt-4o` (edit `.env`)
- Reduce context: Edit `agents.py` and change history limit from 5 to 2
- Use Claude Sonnet (faster than GPT-4o)

### Poor SQL accuracy
**Solutions**:
- Use `gpt-4o` or `claude-sonnet-4-5` (not mini versions)
- Add more examples to the prompts in `agents.py`
- Improve schema descriptions in `schema.py`

---

## 📁 Project Structure

```
sql-ai-agent/
├── data/
│   ├── raw/              # CSV files
│   ├── ecommerce.db      # SQLite database
│   └── schema.json       # Extracted schema
├── src/
│   ├── app.py           # Streamlit UI
│   ├── agents.py        # Multi-agent system
│   ├── database.py      # Database operations
│   ├── validator.py     # Query validation
│   ├── schema.py        # Schema extraction
│   ├── setup_database.py
│   └── download_dataset.py
├── outputs/             # Logs and exports
├── notebooks/           # Jupyter notebooks
├── .env                 # API keys (YOU CREATE THIS)
├── .env.example         # Template
├── requirements.txt
└── README.md
```

---

## 🎬 Recording Your LinkedIn Video

### Before Recording:

1. **Prepare demo queries** that show impressive results:
   ```
   "Show me revenue trends by month"
   "What are the top 10 selling products?"
   "Compare delivery times across states"
   "Which payment methods are most popular?"
   ```

2. **Clear your chat history** for a clean demo

3. **Test everything once** to ensure no errors during recording

### Recording Tips:

1. **Keep it short**: 60-120 seconds ideal
2. **Show, don't tell**: Focus on demos, not code
3. **Tell a story**: Problem → Solution → Demo → Results
4. **Add captions**: Many watch without sound
5. **Hook in first 3 seconds**: "I built an AI agent that..."

### Recording Tools:

- **macOS**: QuickTime (free), ScreenFlow
- **Windows**: OBS Studio (free), Camtasia
- **Linux**: OBS Studio, SimpleScreenRecorder
- **All**: Loom (easiest, web-based)

---

## 🚀 Next Steps

### Customize for Your Portfolio:

1. **Choose different dataset** (see `ALTERNATIVE_DATASETS.md`)
2. **Customize UI colors** in `app.py`
3. **Add your branding** (name, logo in sidebar)
4. **Improve prompts** in `agents.py` for better accuracy
5. **Add features**: Voice input, PDF export, email reports

### Make it Production-Ready:

1. Deploy to Streamlit Cloud (free hosting)
2. Add user authentication
3. Add rate limiting
4. Use PostgreSQL instead of SQLite
5. Add caching for common queries
6. Monitor costs with API usage tracking

### Extend Functionality:

1. **Multi-database support**: Connect to MySQL, PostgreSQL, BigQuery
2. **Report generation**: Auto-generate weekly/monthly reports
3. **Slack/Teams integration**: Query from chat
4. **Voice interface**: Add speech-to-text
5. **Alerts**: Set up notifications for key metrics

---

## 📊 Performance Expectations

### Query Speed:
- Simple queries: 2-5 seconds
- Complex queries: 5-10 seconds
- First query (cold start): 10-15 seconds

### Accuracy:
- Simple queries (COUNT, SUM): ~95%
- Medium complexity (JOINs, GROUP BY): ~85%
- Complex queries (multiple JOINs, subqueries): ~75%

### Cost (per 100 queries):
- GPT-4o: $3-5
- GPT-4o-mini: $0.50-1
- Claude Sonnet: $2-4

---

## 🤝 Getting Help

- **GitHub Issues**: Report bugs or ask questions
- **Documentation**: Check all .md files in project
- **Test scripts**: Run individual component tests
- **Logs**: Check `outputs/` folder for execution logs

---

## ✅ Checklist

Before recording your LinkedIn video:

- [ ] API key configured and working
- [ ] Database set up with all tables
- [ ] App launches without errors
- [ ] Can ask sample questions successfully
- [ ] Visualizations render correctly
- [ ] Prepared 4-5 impressive demo questions
- [ ] Cleaned up chat history
- [ ] Tested screen recording software
- [ ] Written video script/outline

You're ready to build your portfolio project! 🎉
