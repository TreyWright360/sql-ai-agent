# 🚀 Frontend Deployment Guide

Complete guide to deploy your SQL AI Agent frontend to production.

---

## 📋 Pre-Deployment Checklist

Before deploying, customize these files:

### 1. Update Personal Links in `index.html`

**Line 34** - GitHub Repo URL:
```html
<a href="https://github.com/YOURUSERNAME/sql-ai-agent" target="_blank" class="nav-link nav-link-github">
```

**Lines 250-252** - Footer Social Links:
```html
<a href="https://github.com/YOURUSERNAME" target="_blank" class="footer-link">GitHub</a>
<a href="https://linkedin.com/in/YOURPROFILE" target="_blank" class="footer-link">LinkedIn</a>
<a href="https://twitter.com/YOURHANDLE" target="_blank" class="footer-link">Twitter</a>
```

**Line 230** - CTA GitHub Link:
```html
<a href="https://github.com/YOURUSERNAME/sql-ai-agent" target="_blank" class="btn btn-secondary btn-lg">
```

### 2. Configure Backend API in `app.js`

**Lines 2-4** - API Configuration:
```javascript
const CONFIG = {
    API_URL: 'https://your-backend-url.streamlit.app/api/query', // Your deployed backend
    SESSION_ID: generateSessionId(),
};
```

### 3. Test Locally First

```bash
cd frontend

# Option A: Python
python -m http.server 8080

# Option B: Node.js
npx http-server -p 8080

# Open: http://localhost:8080
```

Test these before deploying:
- [ ] All sample query buttons work
- [ ] Chat interface loads
- [ ] Mock responses display correctly
- [ ] Charts render properly
- [ ] Mobile responsive (test in DevTools)
- [ ] All links go to correct URLs

---

## 🎯 Option 1: Vercel Deployment (RECOMMENDED)

### Why Vercel?
✅ **Free forever** for personal projects
✅ **Instant deployment** (<60 seconds)
✅ **Auto HTTPS** and global CDN
✅ **Git integration** - Auto-deploy on push
✅ **Perfect for portfolios**

### Step-by-Step

#### A. Install Vercel CLI

```bash
npm install -g vercel
```

#### B. Login

```bash
vercel login
```

(Opens browser, authenticate with GitHub)

#### C. Deploy

```bash
cd frontend
vercel
```

Follow prompts:
- **Set up and deploy**: Yes
- **Which scope**: Your account
- **Link to existing project**: No
- **Project name**: sql-ai-agent
- **Directory**: `./`
- **Override settings**: No

**Done!** You'll get a URL like:
```
https://sql-ai-agent-xyz123.vercel.app
```

#### D. Deploy to Production

```bash
vercel --prod
```

Gets you a clean production URL:
```
https://sql-ai-agent.vercel.app
```

### Custom Domain on Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Settings → Domains
4. Add domain: `sql-agent.yourdomain.com`
5. Add DNS records (Vercel provides instructions)

---

## 🟦 Option 2: Netlify Deployment

### Why Netlify?
✅ **Free tier generous**
✅ **Drag-and-drop deployment** (easiest)
✅ **Form handling** (if you add contact form)
✅ **Split testing** built-in

### Method A: Drag and Drop (Easiest)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag your `frontend` folder onto the page
3. **Done!** Get URL like: `random-name-123.netlify.app`

### Method B: Netlify CLI

```bash
# Install
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy

# When ready, deploy to production
netlify deploy --prod
```

### Custom Domain on Netlify

1. Go to [app.netlify.com](https://app.netlify.com)
2. Select your site
3. Domain settings → Add custom domain
4. Follow DNS instructions

---

## 🐙 Option 3: GitHub Pages (Free)

### Why GitHub Pages?
✅ **Completely free**
✅ **No credit card needed**
✅ **Built into GitHub**

### Setup

#### A. Create `gh-pages` Branch

```bash
# From project root
git checkout -b gh-pages

# Copy frontend files to root
cp -r frontend/* .

# Commit
git add .
git commit -m "Deploy to GitHub Pages"

# Push
git push origin gh-pages
```

#### B. Enable GitHub Pages

1. Go to your repo on GitHub
2. Settings → Pages
3. Source: `gh-pages` branch
4. Save

**URL**: `https://yourusername.github.io/sql-ai-agent`

---

## ☁️ Option 4: Cloudflare Pages

### Why Cloudflare?
✅ **Fastest CDN** globally
✅ **Unlimited bandwidth** free
✅ **DDoS protection** included

### Setup

1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Connect GitHub repo
3. Select `frontend` as source directory
4. Deploy

**URL**: `https://sql-ai-agent.pages.dev`

---

## 🔄 CI/CD: Auto-Deploy on Git Push

### Vercel + GitHub

```bash
# Link GitHub repo
vercel --prod

# Now every push to main auto-deploys
git push origin main
```

### Netlify + GitHub

1. New site from Git
2. Connect repository
3. Build settings:
   - Base directory: `frontend`
   - Publish directory: `frontend`
4. Deploy

**Every push to `main` auto-deploys!**

---

## 🎨 Advanced: Environment-Specific Configs

### Create `config.js`

```javascript
// config.js
const ENV = {
    development: {
        API_URL: 'http://localhost:8000/api/query'
    },
    production: {
        API_URL: 'https://your-backend.streamlit.app/api/query'
    }
};

const CONFIG = ENV[window.location.hostname === 'localhost' ? 'development' : 'production'];

export default CONFIG;
```

### Update `app.js`

```javascript
import CONFIG from './config.js';

// Use CONFIG.API_URL
```

### Add to `index.html` `<head>`:

```html
<script type="module" src="config.js"></script>
<script type="module" src="app.js"></script>
```

---

## 🔗 Connecting Frontend to Backend

### If Using Streamlit Backend

Your Streamlit app needs an API endpoint:

```python
# Add to your Streamlit app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/query")
async def query_endpoint(request: dict):
    # Your SQL agent logic here
    return {"response": "...", "data": [...], "visualization": {...}}
```

### If Using FastAPI Backend

Enable CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_methods=["POST"],
    allow_headers=["*"],
)
```

---

## 📊 Analytics Setup (Optional)

### Google Analytics

Add to `index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Vercel Analytics

```bash
npm install @vercel/analytics

# Add to app.js:
import { inject } from '@vercel/analytics';
inject();
```

---

## 🐛 Troubleshooting

### Issue: "CORS Error"

**Solution**: Enable CORS on your backend
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific frontend URL
)
```

### Issue: "404 Not Found" on Vercel

**Solution**: Add `vercel.json` (already included)

### Issue: Charts not rendering

**Solution**: Check browser console. Chart.js CDN may be blocked.

**Fix**: Download Chart.js locally:
```bash
curl https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js > chart.min.js
```

Update `index.html`:
```html
<script src="chart.min.js"></script>
```

### Issue: Mobile layout broken

**Solution**: Check viewport meta tag in `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

---

## ✅ Post-Deployment Checklist

- [ ] **Test live URL** on desktop
- [ ] **Test on mobile** (use browserstack.com)
- [ ] **Check all links** work
- [ ] **Test sample queries** with mock data
- [ ] **Verify social links** go to your profiles
- [ ] **Check page speed** (pagespeed.web.dev)
- [ ] **Test HTTPS** is working
- [ ] **Add URL to resume**
- [ ] **Add URL to LinkedIn profile**
- [ ] **Share in portfolio video**

---

## 🎬 For Your Portfolio Video

### What to Show

1. **Desktop View** (30 seconds):
   - Homepage with hero stats
   - Click "Try Live Demo"
   - Type a sample query
   - Show chart appearing

2. **Mobile View** (10 seconds):
   - Open on phone (use DevTools)
   - Show responsive design

3. **Code Mention** (5 seconds):
   - Flash the GitHub link
   - "Full code available at [URL]"

### Recording Tips

- Browser zoom: 125%
- Hide bookmarks bar
- Close other tabs
- Use incognito mode (clean cookies)
- Screen resolution: 1920x1080

---

## 🚀 Launch Sequence

### Day 1: Deploy
```bash
cd frontend
vercel --prod
```

### Day 2: Test
- [ ] Desktop browser test
- [ ] Mobile browser test
- [ ] Share with 3 friends for feedback

### Day 3: Optimize
- [ ] Fix any reported bugs
- [ ] Add analytics
- [ ] Speed test and optimize

### Day 4: Promote
- [ ] Add to resume
- [ ] Update LinkedIn
- [ ] Record demo video
- [ ] Post on social media

---

## 📈 Monitoring

### Check Uptime

- **UptimeRobot** (free): Monitor your URL
- **Pingdom**: Performance monitoring
- **Vercel Analytics**: Built-in (if using Vercel)

### Track Visitors

- **Google Analytics**: See where traffic comes from
- **Vercel Analytics**: Simple visitor count
- **Hotjar**: See how users interact (heatmaps)

---

## 💡 Pro Tips

1. **Short URL**: Use bit.ly for resume/LinkedIn
   - Example: `bit.ly/sql-ai-agent` → `https://sql-ai-agent.vercel.app`

2. **QR Code**: Generate QR code for business cards
   - Use: qr-code-generator.com

3. **OG Tags**: Add for better LinkedIn previews
   ```html
   <meta property="og:title" content="SQL AI Agent">
   <meta property="og:description" content="Query databases in natural language">
   <meta property="og:image" content="https://your-url/preview.png">
   ```

4. **Favicon**: Use emoji favicon for simplicity (already included)

5. **Performance**: Run Lighthouse audit
   ```bash
   npm install -g lighthouse
   lighthouse https://your-url.vercel.app
   ```

---

## 🎓 Next Steps

After deployment:

1. **Add to Portfolio Site**: Embed demo link
2. **Write Blog Post**: "Building an AI SQL Agent"
3. **Create Tutorial**: Longer YouTube walkthrough
4. **Open Source**: Accept contributions on GitHub
5. **Iterate**: Add features based on feedback

---

## 📞 Need Help?

- **Deployment issues**: Check Vercel/Netlify docs
- **Frontend bugs**: Open GitHub issue
- **General questions**: Connect on [LinkedIn](https://linkedin.com/in/yourprofile)

---

**You're ready to deploy! Pick your platform and ship it! 🚀**

Recommended: Start with Vercel (easiest, fastest, free forever).

```bash
cd frontend
vercel --prod
```

**Good luck!** 🎉
