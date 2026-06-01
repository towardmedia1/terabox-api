# 🚀 Deployment Guide

## Step-by-Step Deployment Instructions

### 1️⃣ Deploy API to Render

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Terabox API with frontend"
   git push origin main
   ```

2. **Create Render Account:**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repo

4. **Configure Service:**
   - **Name:** `terabox-api` (or your choice)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Copy your API URL: `https://terabox-api-xxxx.onrender.com`

---

### 2️⃣ Update Frontend with Your API URL

1. **Open `index.html`**

2. **Find this line (around line 145):**
   ```javascript
   const API_URL = 'https://onrender.com/api/v1/fetch';
   ```

3. **Replace with your actual Render URL:**
   ```javascript
   const API_URL = 'https://terabox-api-xxxx.onrender.com/api/v1/fetch';
   ```

4. **Save the file**

---

### 3️⃣ Deploy Frontend

#### Option A: GitHub Pages (Recommended - Free & Easy)

1. **Create `gh-pages` branch:**
   ```bash
   git checkout -b gh-pages
   ```

2. **Keep only frontend files:**
   ```bash
   # Create a simple index at root
   git add index.html
   git commit -m "Frontend for GitHub Pages"
   git push origin gh-pages
   ```

3. **Enable GitHub Pages:**
   - Go to your repo → Settings → Pages
   - Source: `gh-pages` branch
   - Save

4. **Access your site:**
   - `https://your-username.github.io/your-repo-name/`

#### Option B: Netlify (Alternative)

1. **Go to https://netlify.com**
2. **Drag & drop `index.html`**
3. **Done!** Get instant URL

#### Option C: Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

---

### 4️⃣ Test Your Deployment

1. **Test API:**
   ```bash
   curl "https://your-api.onrender.com/health"
   ```

2. **Test Frontend:**
   - Open your frontend URL
   - Paste a Terabox link
   - Click "Get Download Links"
   - Should see results!

---

## 🔧 Troubleshooting

### API Issues

**Problem:** API returns 503 error
- **Solution:** Render free tier sleeps after inactivity. First request takes 30s to wake up.

**Problem:** CORS error
- **Solution:** Make sure CORS middleware is enabled in `api_server.py`

**Problem:** "All endpoints failed"
- **Solution:** Terabox might be blocking. Try with VPN or update cookie pool.

### Frontend Issues

**Problem:** "Network error"
- **Solution:** Check if API URL in `index.html` is correct

**Problem:** Blank page
- **Solution:** Check browser console for errors. Ensure Tailwind CDN is loading.

---

## 📊 Monitoring

### Check API Status
```bash
curl https://your-api.onrender.com/health
```

### View API Logs
- Go to Render Dashboard
- Select your service
- Click "Logs" tab

---

## 🔄 Updates

### Update API Code
```bash
git add .
git commit -m "Update API"
git push origin main
```
Render auto-deploys on push!

### Update Frontend
```bash
# Update index.html
git add index.html
git commit -m "Update frontend"
git push origin gh-pages  # or main, depending on setup
```

---

## 💡 Pro Tips

1. **Custom Domain:**
   - Render: Settings → Custom Domain
   - GitHub Pages: Settings → Pages → Custom domain

2. **Environment Variables:**
   - Add in Render Dashboard → Environment
   - Example: `COOKIE_POOL=cookie1,cookie2`

3. **Performance:**
   - Use Render's paid plan to avoid cold starts
   - Enable caching headers

4. **Security:**
   - Add rate limiting
   - Use environment variables for sensitive data
   - Enable HTTPS (automatic on Render)

---

## 🎯 Quick Links

- **Render Dashboard:** https://dashboard.render.com
- **GitHub Pages:** https://pages.github.com
- **Netlify:** https://netlify.com
- **Vercel:** https://vercel.com

---

## ✅ Checklist

- [ ] API deployed to Render
- [ ] API URL copied
- [ ] `index.html` updated with API URL
- [ ] Frontend deployed
- [ ] Tested with real Terabox link
- [ ] Shared with friends! 🎉

---

**Need Help?** Check the main README.md or open an issue on GitHub.
