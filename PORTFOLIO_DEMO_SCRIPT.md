# Portfolio Demo Script & Video Guide 🎬

**Goal:** Create a high-impact, 90-120 second video demonstration of your SQL AI Agent that proves your skills to recruiters and hiring managers.

---

## 📋 Pre-Recording Checklist
*   **Resolution:** Record in 1080p (1920x1080).
*   **Audio:** Use a decent mic, minimize background noise.
*   **Screen:** Clean up your desktop. Close unrelated tabs.
*   **Theme:** Use Dark Mode in your IDE/Browser if possible (looks more premium).
*   **Zoom:** Zoom in your browser to 125% so text is readable on mobile.

---

## 📝 Video Structure (The "6-Act" Structure)

| Segment | Time | Purpose |
| :--- | :--- | :--- |
| **1. The Hook** | 0:00 - 0:10 | Grab attention immediately with the value prop. |
| **2. The Problem** | 0:10 - 0:25 | Explain *why* you built this (business value). |
| **3. The Solution** | 0:25 - 0:45 | High-level architecture explanation. |
| **4. The Demo** | 0:45 - 1:40 | Show, don't just tell. 3 specific queries. |
| **5. The Tech** | 1:40 - 1:50 | Flash the tech stack (Logos/Code). |
| **6. Call to Action** | 1:50 - 2:00 | Tell them what to do next. |

---

## 🎙️ Word-for-Word Scripts

### Option A: The "Confident Engineer" (Recommended)
*Best for general software engineering/data engineering roles.*

**(0:00) Hook**
"I built an AI agent that allows non-technical users to query a database of 100,000 orders using plain English, with 87% accuracy."

**(0:10) Problem**
"We all know the bottleneck: Business users need data, but they don't know SQL. They have to wait days for analysts to write simple queries. Dashboard tools are static; they can't answer ad-hoc questions."

**(0:25) Solution**
"I solved this by building a multi-agent system. It doesn't just match keywords. It understands the database schema, validates the SQL for security to ensure it's read-only, and then visualizes the results."

**(0:45) The Demo**
*(Action: Show the screen. Type the first query)*
"Let's look at a simple example. 'Show me the top 5 customers by revenue in 2023.' You can see it generates the complex JOINs instantly."

*(Action: Run a harder query)*
"Now let's try something harder. 'Calculate the month-over-month growth for creating visualization.' It handles the aggregations and window functions correctly."

*(Action: Show the 'Reasoning' or 'SQL' tab)*
"Crucially, it shows its work here, so we can trust the result."

**(1:40) Tech Stack**
"This is built with Python, LangChain, and OpenAI, with a custom Streamlit frontend and a Supabase backend."

**(1:50) CTA**
"The full code and a live demo link are in the description. Thanks for watching."

---

### Option B: The "Storyteller"
*Best for Product Manager or client-facing roles.*

**(0:00) Hook**
"Imagine asking your database questions as easily as you ask a colleague. That's what I've built."

**(0:10) Problem**
"In my last role, I saw managers struggling to get simple numbers. 'How many T-shirts did we sell in black vs white?' Simple question, but it required a data ticket."

... *(Continue with more focus on user experience and business impact)*

---

## 🔍 The Demo Queries to Use

Don't just use random queries. Use these **3 Specific Tiers** to show depth.

### Tier 1: The "Sanity Check" (Simple)
*Proves it works.*
> "Show me all unique products in the electronics category."
*   **Why**: Fast, easy to verify visually.

### Tier 2: The "Business Value" (Aggregations + Joins)
*Proves it understands relationships.*
> "Who are the top 3 customers by total spend in 2024?"
*   **Why**: Requires joining `Customers` and `Orders` tables and summing values.

### Tier 3: The "Complex Logic" (Date Math / Logic)
*Proves it's robust.*
> "Show me the monthly revenue trend for the last 12 months."
*   **Why**: Requires date formatting and grouping. Perfect if your app outputs a chart!

---

## 🛠️ Production Tips

### 1. The "Pause and Crop" Technique
Don't try to record it all in one take.
1. Record the Hook. Stop.
2. Record the Problem. Stop.
3. Record the screen capture for the Demo. Stop.
4. Stitch them together in CapCut or Premiere.
*It makes you sound much more articulate and removes 'umms' and 'ahhs'.*

### 2. Audio is King
If your voice sounds echoey, put a blanket over your head (seriously) or record in a closet full of clothes. Bad audio ruins good code demos.

### 3. Mouse Movement
During the screen recording, keep your mouse **still** when you aren't clicking. Don't wave it around while talking. It's distracting.

### 4. Background Music
Add a very subtle "Lo-Fi Beats" or "Tech Corporate" track at 10% volume. It fills the silence and makes verify professional.

---

## 📱 Platform Specific Advice

### LinkedIn
*   **Caption**: Use the template in `PORTFOLIO_PACKAGE_README.md`.
*   **Format**: Square (1:1) or Portait (4:5) works best, but Landscape (16:9) is fine for code.
*   **Tagging**: Tag @LangChain, @Streamlit, or any tools you used. They often repost good projects!

### YouTube
*   **Title**: "I built an AI SQL Analyst (Python & LangChain Project)"
*   **Thumbnail**: A picture of you + a screenshot of the UI + text "AI SQL AGENT".
*   **Description**: Put the GITHUB LINK at the very top.

### Twitter / X
*   **Format**: Short clips work better. Maybe just post the "Demo" segment (45s) as a teaser.
