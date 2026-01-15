# Codebasics Portfolio Project Workflow
## From Concept to LinkedIn-Ready in 7 Days

This guide follows the **Codebasics methodology** for creating portfolio projects that get you noticed by recruiters and hiring managers.

---

## 📅 Week-by-Week Breakdown

### **Day 1-2: Planning & Dataset Selection** 🎯

#### What to Do:

1. **Choose Your Dataset** (See `ALTERNATIVE_DATASETS.md`)
   - Pick based on your target role:
     - Data Analyst → Instacart, Superstore
     - Business Analyst → Rossmann, Northwind
     - Data Engineer → H&M, Adventure Works

2. **Define Your Story**
   - **Problem**: What business problem are you solving?
   - **Solution**: How does your AI agent help?
   - **Impact**: What value does it provide?

   **Example Story**:
   ```
   Problem: "Business analysts spend hours writing SQL queries"
   Solution: "Built an AI agent that converts plain English to SQL"
   Impact: "Reduces query time from 30 minutes to 30 seconds"
   ```

3. **Set Project Scope**
   - Core features (MUST have):
     - [ ] Natural language to SQL
     - [ ] Query validation (security)
     - [ ] Auto-visualizations
     - [ ] Chat history

   - Nice-to-have features:
     - [ ] Voice input
     - [ ] PDF export
     - [ ] Email reports
     - [ ] Slack integration

   **Codebasics Tip**: Start with core features. Add extras only if time permits.

4. **Create Project Brief**

Create a file `PROJECT_BRIEF.md`:

```markdown
# Project: [Your Project Name]

## Overview
AI-powered SQL query agent for [industry/dataset]

## Dataset
- Name: [Dataset name]
- Size: [X million rows]
- Tables: [Number]
- Domain: [E-commerce/Retail/etc.]

## Target Audience
- Business analysts
- Product managers
- Non-technical stakeholders

## Key Features
1. Natural language queries
2. Auto-visualizations
3. Query validation
4. Session management

## Success Metrics
- Accuracy: 85%+ correct SQL
- Speed: <5 seconds per query
- Safety: 100% destructive query prevention

## Timeline
- Setup: Day 1-2
- Development: Day 3-5
- Testing & Polish: Day 6
- Video & Documentation: Day 7
```

---

### **Day 3-4: Setup & Development** 💻

#### Day 3 Morning: Environment Setup

```bash
# 1. Set up project
cd training/sql-ai-agent
./quickstart.sh

# 2. Download YOUR chosen dataset
# Follow instructions in ALTERNATIVE_DATASETS.md

# 3. Customize for your dataset
# Edit src/setup_database.py with your table names
```

#### Day 3 Afternoon: Test Core System

```bash
# Test each component
python src/validator.py    # Should see validation tests pass
python src/database.py     # Should see sample queries work
python src/schema.py       # Should generate schema.json
python src/agents.py       # Should see AI responses
```

**✅ Checkpoint**: All 4 tests passing = ready to proceed

#### Day 4: Customize & Enhance

1. **Customize UI** (`src/app.py`)
   ```python
   # Update line 14-16 with your branding
   st.set_page_config(
       page_title="[Your Project Name]",
       page_icon="🤖",  # Choose your emoji
   )

   # Update sidebar info (line 144-150)
   st.info("""
   **[Your Dataset Name]**
   - [X] rows
   - [Y] tables
   - [Year range]
   """)
   ```

2. **Improve Prompts** (`src/agents.py`)
   - Add domain-specific examples
   - Include common business questions
   - Improve response format

3. **Test with Real Questions**

   Create `test_queries.txt`:
   ```
   How many orders are there?
   Show me revenue by month
   What are the top 10 products?
   Compare [metric] across [dimension]
   Which [category] has the highest [metric]?
   ```

   Test each one and note:
   - ✅ Correct SQL generated
   - ✅ Correct results returned
   - ✅ Appropriate visualization
   - ❌ Errors or inaccuracies

**✅ Checkpoint**: 80%+ of test queries work correctly

---

### **Day 5: Testing & Bug Fixes** 🐛

#### Morning: Edge Case Testing

Test these scenarios:
1. **Ambiguous questions**: "Show me sales" (sales of what? when?)
2. **Invalid requests**: "Delete all orders"
3. **Complex queries**: Multiple joins, aggregations
4. **Follow-up questions**: "Show more details" after first query
5. **Out of scope**: "What's the weather?"

**Fix common issues**:
- Ambiguous → Improve prompt to ask for clarification
- Invalid → Validator should block (it should already work)
- Complex → Add examples to SQL agent prompt
- Follow-ups → Ensure chat history is working
- Out of scope → Add response: "I can only answer questions about [dataset]"

#### Afternoon: Performance Optimization

1. **Measure Response Time**
   ```python
   # Add timing to agents.py
   import time
   start = time.time()
   # ... process query ...
   elapsed = time.time() - start
   print(f"Query took {elapsed:.2f}s")
   ```

2. **Optimize if slow** (>10 seconds):
   - Reduce chat history context (5 → 2 messages)
   - Use faster model (gpt-4o-mini)
   - Add LIMIT to generated queries
   - Cache schema context

3. **Test on Different Devices**
   - Desktop browser
   - Mobile browser
   - Different screen sizes

**✅ Checkpoint**: App works smoothly, <5s response time for simple queries

---

### **Day 6: Polish & Documentation** ✨

#### Morning: UI Polish

1. **Add Sample Questions** relevant to YOUR dataset
   ```python
   # In app.py, update sample_queries list
   sample_queries = [
       "[Specific question about your dataset]",
       "[Question that shows complex query]",
       "[Question that creates nice visualization]",
       "[Business-focused question]",
       "[Time-series question]",
   ]
   ```

2. **Improve Error Messages**
   - User-friendly language
   - Suggest what to try instead
   - No technical jargon

3. **Add Stats Dashboard** (optional)
   ```python
   # In sidebar, add interesting dataset stats
   st.metric("Total Orders", "3.4M")
   st.metric("Date Range", "2016-2018")
   st.metric("Success Rate", "92%")
   ```

#### Afternoon: Create Documentation

1. **Update README.md** with:
   - Your project name
   - Your dataset description
   - Your unique features
   - Demo screenshots/GIF

2. **Create DEMO_QUERIES.md**
   ```markdown
   # Demo Queries for [Your Project]

   ## Simple Queries
   - "How many orders?"
   - "Show me total revenue"

   ## Analytical Queries
   - "Compare sales by region"
   - "Show monthly trends for 2017"

   ## Complex Queries
   - "What's the correlation between delivery time and rating?"
   - "Which products are frequently bought together?"
   ```

3. **Take Screenshots**
   - Clean interface (no chat history)
   - Example query with nice visualization
   - Data table view
   - SQL query view

**✅ Checkpoint**: Documentation is clear, screenshots look professional

---

### **Day 7: Video & LinkedIn Post** 🎬

#### Morning: Create Demo Video

**Video Structure** (90-120 seconds):

1. **Hook** (0:00-0:05)
   - "I built an AI agent that queries [X] million rows..."
   - Show impressive number on screen

2. **Problem** (0:05-0:20)
   - "Writing SQL is hard..."
   - "Business users want insights without coding..."
   - Show frustrated person or complex SQL

3. **Solution** (0:20-0:40)
   - "So I built this multi-agent system"
   - Quick architecture diagram (optional)
   - List 3-4 key features with icons

4. **Demo** (0:40-1:30)
   - **Query 1** (Simple): "How many orders?"
     - Show typing, instant result
   - **Query 2** (Visualization): "Show revenue trends"
     - Show beautiful chart appearing
   - **Query 3** (Complex): "Top products by category"
     - Show data table + chart
   - **Bonus**: Click "View SQL" to show generated query

5. **Tech Stack** (1:30-1:45)
   - Quick list: Python, LangChain, GPT-4, Streamlit
   - Mention key feature: "Query validation prevents data corruption"

6. **CTA** (1:45-2:00)
   - "Code on GitHub [link in comments]"
   - "Building in public, follow for more"
   - Your social handles

**Recording Tips**:
- Clean browser (close tabs)
- Clear chat history
- Zoom in (125-150%)
- Hide cursor when not needed
- Add gentle background music
- Use captions (critical!)

**Tools**:
- Recording: Loom, OBS, ScreenFlow
- Editing: iMovie, DaVinci Resolve (free)
- Captions: Kapwing, Descript

#### Afternoon: LinkedIn Post

**Post Template**:

```
🤖 I built an AI agent that queries [X] million rows of [domain] data

[Problem you solved in 1 sentence]

Here's what I built:
✅ [Feature 1]
✅ [Feature 2]
✅ [Feature 3]
✅ [Feature 4]

Tech stack:
🔹 [Main tech 1]
🔹 [Main tech 2]
🔹 [Main tech 3]

The most interesting challenge was [specific technical challenge you solved].

[Key insight or learning]

🔗 Full demo in the video 👆
💻 Code on GitHub: [link]

Building in public. What should I add next?

#DataScience #AI #Portfolio #MachineLearning #Python
```

**Example Post**:

```
🤖 I built an AI agent that queries 3 million grocery orders in plain English

SQL is powerful, but most business users don't know it. So I built an AI agent that lets anyone ask questions about data using natural language.

Here's what it does:
✅ Converts English → SQL automatically
✅ Generates charts & visualizations
✅ Validates queries for safety (no accidental deletes!)
✅ Remembers conversation context

Tech stack:
🔹 Python + LangChain
🔹 GPT-4 with reasoning
🔹 Streamlit for UI
🔹 Query validation layer

The most interesting challenge was ensuring the AI never generates destructive queries (DELETE, DROP, etc.). Built a validator that catches these before execution.

Accuracy is ~87% on complex multi-table joins. Not perfect, but impressive for natural language.

🔗 Full demo in the video 👆
💻 Code on GitHub: [link in comments]

What dataset should I tackle next?

#DataScience #AI #Portfolio #SQLAgent #Python #LangChain
```

**Posting Strategy**:

1. **First comment**: Add GitHub link (LinkedIn penalizes links in main post)
   ```
   GitHub: [your link]
   Dataset: [dataset link]
   Tutorial: [if you make one]
   ```

2. **Second comment**: Tag relevant people/companies
   ```
   Inspired by @[original creator]
   Built with @LangChainAI @OpenAI
   Dataset from @[dataset source]
   ```

3. **Engage**: Respond to ALL comments in first 2 hours

4. **Cross-post**: Twitter, Dev.to, Medium (repurpose content)

**✅ Checkpoint**: Video posted, GitHub repo linked, engaging with comments

---

## 📊 Portfolio Project Checklist

### Before Publishing:

**Code Quality**:
- [ ] No hardcoded API keys (use .env)
- [ ] No print statements (use logging)
- [ ] Requirements.txt is complete
- [ ] All test scripts pass
- [ ] Error handling for common issues

**Documentation**:
- [ ] README with setup instructions
- [ ] Screenshot/GIF in README
- [ ] Comments in complex code sections
- [ ] DEMO_QUERIES.md with examples
- [ ] LICENSE file (MIT recommended)

**GitHub Repo**:
- [ ] Descriptive repo name
- [ ] Good README with badges
- [ ] Topics/tags added
- [ ] .gitignore (don't commit .env, .db files)
- [ ] Professional commit messages

**Video**:
- [ ] Under 2 minutes
- [ ] Captions added
- [ ] Good audio quality
- [ ] Shows actual working demo
- [ ] Includes CTA

**LinkedIn Post**:
- [ ] Catchy hook
- [ ] Clear problem/solution
- [ ] Technical but accessible
- [ ] GitHub link in comments
- [ ] Relevant hashtags (5-8)

---

## 🎯 Codebasics Success Criteria

Your project is **portfolio-ready** when:

1. **Technical Excellence**
   - Works without errors
   - Handles edge cases
   - Secure (query validation)
   - Well-documented code

2. **Business Value**
   - Solves real problem
   - Clear use case
   - Measurable impact
   - Professional presentation

3. **Communication**
   - Clear documentation
   - Professional video
   - Engaging LinkedIn post
   - Active in comments

4. **Uniqueness**
   - Different dataset than tutorial
   - Custom features
   - Your own insights
   - Personal branding

---

## 💡 Pro Tips from Codebasics Style

1. **Start with "Why"**
   - Don't just show what you built
   - Explain WHY you built it
   - What problem does it solve?

2. **Show Your Process**
   - Share challenges you faced
   - How you overcame them
   - What you learned
   - Builds authenticity

3. **Make it Interactive**
   - Ask questions in post
   - "What should I add next?"
   - "What dataset should I try?"
   - Drives engagement

4. **Document as You Build**
   - Don't wait until end
   - Take screenshots during development
   - Note interesting bugs/solutions
   - Makes video creation easier

5. **Quality > Quantity**
   - Better to have 1 amazing project
   - Than 10 mediocre ones
   - Focus on polish

6. **Be Consistent**
   - Post regularly (weekly)
   - Build in public
   - Share learnings
   - Grow your network

---

## 📈 What Happens After Posting

**Week 1**:
- Respond to all comments
- Share in relevant groups
- Cross-post to other platforms
- Track engagement metrics

**Week 2-4**:
- Iterate based on feedback
- Add requested features
- Write blog post (long-form)
- Consider YouTube tutorial

**Long-term**:
- Add to resume
- Mention in interviews
- Use in portfolio website
- Build similar projects

---

## 🎓 Resume Bullet Points

Transform your project into resume bullets:

**Before** (Weak):
- Built SQL chatbot using Python

**After** (Strong):
- Engineered multi-agent AI system to convert natural language to SQL, processing 3M+ records with 87% accuracy, reducing query time from 30 minutes to 30 seconds
- Implemented query validation layer preventing destructive operations, ensuring 100% data safety across 9 interconnected database tables
- Designed auto-visualization engine generating dynamic charts (bar/line/pie) based on data patterns, improving insight discovery by 60%

**Formula**: [Action Verb] + [What] + [How] + [Impact/Result]

---

## 🚀 You're Ready!

You now have:
- ✅ Complete working system
- ✅ Customized for your dataset
- ✅ Professional documentation
- ✅ Demo video
- ✅ LinkedIn strategy
- ✅ Resume bullets

**Next Steps**:
1. Follow this workflow day-by-day
2. Don't skip the planning phase
3. Focus on polish
4. Ship it!

Remember: **Done is better than perfect**. Ship your project, get feedback, iterate.

Good luck! 🎉

---

## 📚 Additional Resources

- **Codebasics YouTube**: Full portfolio project tutorials
- **This project's docs**:
  - `SETUP_GUIDE.md` - Technical setup
  - `ALTERNATIVE_DATASETS.md` - Dataset options
  - `README.md` - Project overview
- **Tools**:
  - Loom: Screen recording
  - Canva: Thumbnails
  - Grammarly: Writing
  - GitHub: Version control
