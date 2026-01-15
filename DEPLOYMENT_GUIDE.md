# Deployment Guide 🚀

**Goal:** Get your SQL AI Agent live on the web so you can include a clickable link in your resume and LinkedIn profile.

---

## 🏗️ Deployment Options

| Option | Cost | Difficulty | Best For |
| :--- | :--- | :--- | :--- |
| **1. Streamlit Cloud** | **Free** | ⭐ (Easy) | **Portfolios** (Recommended). Easiest setup, native support. |
| **2. Modal** | Free Tier | ⭐⭐ (Medium) | Backend-heavy apps or if you need custom containers. |
| **3. Railway/Render** | ~$5/mo | ⭐⭐⭐ (Hard) | Full production apps with complex databases. |
| **4. Vercel** | Free Tier | ⭐⭐⭐ (Hard) | If you built a custom React frontend (not Streamlit). |

---

## 🌟 Option 1: Streamlit Cloud (Recommended)

This is the "Happy Path". It takes < 15 minutes.

### Step 1: Prepare Your Code
1.  **Requirements File**: Ensure you have a `requirements.txt` file in your root folder.
    ```text
    streamlit
    langchain
    langchain-community
    langchain-openai
    pymysql
    python-dotenv
    # Add any other libraries you imported
    ```
2.  **Secrets Management**: ensure you are NOT hardcoding API keys in your code.
    *   BAD: `api_key = "sk-12345"`
    *   GOOD: `api_key = st.secrets["OPENAI_API_KEY"]`
    *   *Note: Streamlit Cloud uses `st.secrets`, local dev uses `.env`.*

### Step 2: Push to GitHub
1.  Create a new repository on GitHub (e.g., `sql-ai-agent`).
2.  Push your code there.
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/sql-ai-agent.git
    git push -u origin main
    ```

### Step 3: Connect Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io) and sign up with GitHub.
2.  Click **"New app"**.
3.  Select your `sql-ai-agent` repository.
4.  Select the **Main file path** (e.g., `app.py` or `main.py`).
5.  **IMPOTANT:** Click **"Advanced settings"** before deploying.

### Step 4: Add Secrets
In the "Advanced settings" modal, find the "Secrets" field. Paste your `.env` content here in TOML format:

```toml
OPENAI_API_KEY = "sk-proj-..."
DB_HOST = "..."
DB_USER = "..."
DB_PASSWORD = "..."
DB_NAME = "..."
```

### Step 5: Deploy!
Click **"Deploy"**. Watch the oven bake. 🥧
Once it's done, you'll get a URL like `https://sql-ai-agent.streamlit.app`.

---

## 🔒 Security Checklist (Crucial)

Before you share the link publicly, verify these 3 things:

1.  **Read-Only Database User**:
    *   Ensure the `DB_USER` you provided in secrets has **SELECT privileges ONLY**.
    *   Run: `REVOKE INSERT, UPDATE, DELETE ON *.* FROM 'your_user'@'%';` on your database.
    *   *Why?* You don't want a random internet user telling your agent to `DROP TABLE orders;`.

2.  **Budget Limits**:
    *   Set a "Hard Limit" on your OpenAI account (e.g., $10/month).
    *   This prevents a "DoS by Wallet" attack where someone spams your bot to drain your credits.

3.  **Hide Tracebacks**:
    *   In your `app.py`, add `st.set_option('client.showErrorDetails', False)` or handle exceptions gracefully so users don't see raw Python errors.

---

## 🛠️ Troubleshooting

**"ModuleNotFoundError"**
*   You forgot to add a library to `requirements.txt`. Check your imports.

**"Access Denied for user..."**
*   Your database likely doesn't allow connections from the internet (Streamlit's IP).
*   *Fix:* If using a local MySQL, you need to migrate to a cloud DB (Supabase, PlanetScale, or AWS RDS).
    *   **Supabase** is easiest for free PostgreSQL.
    *   **TiDB** or **PlanetScale** are great for MySQL compatibility.

**"App is sleeping"**
*   Streamlit puts free apps to sleep after inactivity. It wakes up when someone visits, but takes ~10s. This is normal for the free tier.

---

## 🌐 Moving to Production (Advanced)

If you want to go beyond the free portfolio tier:

**Option 2: Modal (Serverless)**
1.  Install Modal: `pip install modal`
2.  Create `modal_app.py` wrapping your agent.
3.  Deploy: `modal deploy modal_app.py`
*Good for: High performance, custom environments.*

**Option 3: Docker + Railway**
1.  Create a `Dockerfile`.
2.  Connect GitHub to Railway.app.
3.  Railway automatically builds and deploys.
*Good for: "Always on" apps that shouldn't sleep.*
