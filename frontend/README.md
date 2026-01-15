# SQL AI Agent - Modern Frontend

A beautiful, responsive web interface for the SQL AI Agent portfolio project.

## ✨ Features

- 🎨 **Modern Dark UI** - Professional gradient design
- 💬 **Interactive Chat** - Real-time conversation interface
- 📊 **Auto-Visualizations** - Chart.js powered bar/line/pie charts
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- ⚡ **Fast & Lightweight** - Vanilla JavaScript, no heavy frameworks
- 🎯 **Demo Mode** - Works standalone with mock data

---

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Navigate to frontend directory
cd frontend

# Serve with Python
python -m http.server 8080

# Or use Node.js
npx http-server -p 8080

# Open browser
open http://localhost:8080
```

### Option 2: Deploy to Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Follow prompts, get live URL in 60 seconds
```

### Option 3: Deploy to Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify deploy

# For production
netlify deploy --prod
```

---

## 🔧 Configuration

### Connecting to Your Backend

Edit `app.js` line 2-4:

```javascript
const CONFIG = {
    API_URL: 'https://your-backend-url.com/api/query', // Your FastAPI or Streamlit backend
    SESSION_ID: generateSessionId(),
};
```

### Backend API Format

Your backend should accept POST requests with this format:

**Request:**
```json
{
    "query": "Show me top products",
    "session_id": "session_123"
}
```

**Response:**
```json
{
    "response": "Here are the top products...",
    "data": [
        {"product": "Laptop", "sales": 45000},
        {"product": "Phone", "sales": 38000}
    ],
    "visualization": {
        "type": "bar",
        "title": "Top Products"
    }
}
```

---

## 📁 Project Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # All styling (dark theme, responsive)
├── app.js              # JavaScript logic (API calls, charts)
├── README.md           # This file
└── vercel.json         # Vercel deployment config (optional)
```

---

## 🎨 Customization

### Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --primary: #1f77b4;        /* Main brand color */
    --bg-primary: #0a0e27;     /* Background */
    --text-primary: #ffffff;    /* Text color */
}
```

### Sample Queries

Edit `index.html` lines 130-146 to add your own sample queries.

### Mock Data

Edit `app.js` function `getMockResponse()` to customize demo responses.

---

## 🌐 Deployment Options

| Platform | Cost | Speed | Best For |
|----------|------|-------|----------|
| **Vercel** | Free | ⚡ Instant | Recommended for portfolios |
| **Netlify** | Free | ⚡ Instant | Alternative to Vercel |
| **GitHub Pages** | Free | Fast | Simple static hosting |
| **Cloudflare Pages** | Free | ⚡ Instant | Global CDN |

---

## 🔗 Deployment Commands

### Vercel
```bash
cd frontend
vercel --prod
```

### Netlify
```bash
cd frontend
netlify deploy --prod --dir=.
```

### GitHub Pages
```bash
# Push frontend folder to gh-pages branch
git subtree push --prefix frontend origin gh-pages
```

---

## 📱 Mobile Optimization

The frontend is fully responsive:
- ✅ Mobile-first design
- ✅ Touch-friendly buttons
- ✅ Readable text sizes
- ✅ Optimized charts for small screens

Test responsiveness:
1. Open in Chrome DevTools
2. Toggle device toolbar (Cmd+Shift+M)
3. Test on iPhone, iPad, Android

---

## 🐛 Troubleshooting

### "API request failed"
- Check your `CONFIG.API_URL` in `app.js`
- Ensure backend is running and accessible
- Check CORS settings on backend

### Charts not displaying
- Open browser console (F12)
- Check for Chart.js CDN errors
- Verify data format matches expected structure

### Styling looks broken
- Hard refresh: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)
- Check `styles.css` is loading
- Verify Google Fonts CDN is accessible

---

## 🎯 For Portfolio Presentation

### Before Recording Video:
1. ✅ Update GitHub URL in `index.html` (line 34)
2. ✅ Update social links in footer (lines 250-252)
3. ✅ Test all sample queries work
4. ✅ Set browser zoom to 125%
5. ✅ Clear chat history before demo

### Deployment Checklist:
- [ ] Backend API URL configured
- [ ] All links point to your profiles
- [ ] GitHub repo is public
- [ ] Custom domain set up (optional)
- [ ] HTTPS enabled
- [ ] Mobile tested

---

## 💡 Pro Tips

1. **Custom Domain**: Point `sql-agent.yourdomain.com` to your Vercel deployment
2. **Analytics**: Add Google Analytics to track visits
3. **SEO**: Update meta tags in `<head>` for better LinkedIn previews
4. **Performance**: Images are optimized, no heavy dependencies
5. **A/B Testing**: Try different color schemes for engagement

---

## 🔒 Security

- ✅ No API keys in frontend code
- ✅ All API calls go through backend
- ✅ Input sanitization in place
- ✅ XSS protection via DOM methods

---

## 🤝 Contributing

Want to improve the frontend?

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT License - Free for personal and commercial use.

---

## 🙏 Credits

- **Design Inspiration**: Modern SaaS landing pages
- **Icons**: Emoji (universal, no licensing needed)
- **Charts**: Chart.js (Open source)
- **Fonts**: Inter from Google Fonts

---

## 📞 Questions?

- **Setup issues**: Check troubleshooting section above
- **Feature requests**: Open an issue on GitHub
- **Want to connect**: [LinkedIn](https://linkedin.com/in/yourprofile) | [Twitter](https://twitter.com/yourhandle)

---

**Built with ❤️ for the Codebasics Portfolio Project Series**

Ready to deploy? Run `vercel` in this directory! 🚀
