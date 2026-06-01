# 📤 Manual Deploy Guide (No Git Required)

## ✅ CORS is Already Enabled!

Your `api_server.py` has full CORS support configured. No changes needed!

---

## 🚀 Deploy Without Git (Easy Method)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `terabox-downloader` (or your choice)
3. Description: "Cookie-free Terabox downloader API"
4. Public or Private: Your choice
5. **Don't** initialize with README
6. Click "Create repository"

### Step 2: Upload Files to GitHub

1. On the repository page, click **"uploading an existing file"**

2. **Drag and drop these files:**
   - `api_server.py` ⭐ (Main API)
   - `terabox_bypass.py` (Bypass module)
   - `requirements.txt` (Dependencies)
   - `Procfile` (Deployment config)
   - `index.html` (Frontend)
   - `README.md` (Documentation)
   - `.gitignore` (Git ignore rules)

3. **Commit message:** "Initial commit: Terabox downloader with CORS"

4. Click **"Commit changes"**

5. ✅ Done! Files are now on GitHub

### Step 3: Deploy to Render

1. **Go to Render:**
   - https://dashboard.render.com
   - Sign up with GitHub (free)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Click "Connect account" (if first time)
   - Select your repository: `terabox-downloader`

3. **Configure Service:**
   ```
   Name: terabox-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn api_server:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

4. **Click "Create Web Service"**

5. **Wait 2-3 minutes** for deployment

6. **Copy your API URL:**
   - Example: `https://terabox-api-xxxx.onrender.com`

### Step 4: Update Frontend

1. **Download `index.html` from GitHub** (if you uploaded it)

2. **Open in text editor** (Notepad, VS Code, etc.)

3. **Find line 145:**
   ```javascript
   const API_URL = 'https://onrender.com/api/v1/fetch';
   ```

4. **Replace with your Render URL:**
   ```javascript
   const API_URL = 'https://terabox-api-xxxx.onrender.com/api/v1/fetch';
   ```

5. **Save the file**

6. **Upload updated `index.html` back to GitHub:**
   - Go to your GitHub repository
   - Click on `index.html`
   - Click pencil icon (Edit)
   - Paste updated content
   - Commit changes

### Step 5: Deploy Frontend

#### Option A: GitHub Pages (Recommended)

1. **In your GitHub repository:**
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` → `/root`
   - Save

2. **Wait 1-2 minutes**

3. **Access your site:**
   - `https://YOUR_USERNAME.github.io/terabox-downloader/index.html`

#### Option B: Netlify (Alternative)

1. **Go to:** https://app.netlify.com/drop

2. **Drag `index.html`** into the drop zone

3. **Get instant URL:**
   - Example: `https://random-name-12345.netlify.app`

4. **Done!** Site is live

### Step 6: Test Everything

1. **Open your frontend URL**

2. **Paste a Terabox link:**
   ```
   https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA
   ```

3. **Click "Get Download Links"**

4. **Should see:**
   - Loading spinner
   - File information
   - Download buttons

5. **✅ Success!** Your app is live!

---

## 🔄 Update Your Deployment

### Update API Code

1. **Edit file on GitHub:**
   - Go to repository
   - Click file (e.g., `api_server.py`)
   - Click pencil icon
   - Make changes
   - Commit

2. **Render auto-deploys** in 2-3 minutes

### Update Frontend

1. **Edit `index.html` on GitHub**
2. **Commit changes**
3. **GitHub Pages auto-updates** in 1-2 minutes

---

## 📋 Files to Upload

**Essential Files (Must Upload):**
- ✅ `api_server.py` - Main API
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Deployment config
- ✅ `index.html` - Frontend

**Optional Files (Recommended):**
- `terabox_bypass.py` - Advanced bypass
- `README.md` - Documentation
- `.gitignore` - Git ignore rules

**Don't Upload:**
- ❌ `__pycache__/` folder
- ❌ `.vscode/` folder
- ❌ `*.pyc` files

---

## 🎯 Quick Checklist

- [ ] Created GitHub repository
- [ ] Uploaded all files to GitHub
- [ ] Created Render account
- [ ] Connected GitHub to Render
- [ ] Configured build/start commands
- [ ] Deployment successful
- [ ] Copied Render API URL
- [ ] Updated `index.html` with API URL
- [ ] Uploaded updated `index.html`
- [ ] Deployed frontend (GitHub Pages/Netlify)
- [ ] Tested with real Terabox link
- [ ] Everything works! 🎉

---

## 🐛 Common Issues

### "Build failed on Render"
- Check `requirements.txt` is uploaded
- Verify build command is correct
- Check Render logs for errors

### "CORS error in browser"
- CORS is already configured! ✅
- Check API URL in `index.html` is correct
- Verify API is running (check Render dashboard)

### "No files found"
- Terabox link might be invalid
- Try different link
- Check API logs on Render

### "Frontend not loading"
- Check GitHub Pages is enabled
- Verify `index.html` is in root directory
- Wait 2 minutes for GitHub Pages to update

---

## 📞 Need Help?

**API Issues:**
- Check Render Dashboard → Logs
- Test API: `https://your-app.onrender.com/health`

**Frontend Issues:**
- Check browser console (F12)
- Verify API URL is correct
- Test API separately first

**GitHub Issues:**
- Use GitHub Desktop (easier)
- Or contact GitHub support

---

## ✅ Success Indicators

**API Working:**
- ✅ Render shows "Live"
- ✅ `/health` endpoint responds
- ✅ `/docs` shows API documentation

**Frontend Working:**
- ✅ Page loads without errors
- ✅ Can submit Terabox link
- ✅ Results display correctly
- ✅ Download buttons work

**CORS Working:**
- ✅ No CORS errors in console
- ✅ API requests succeed
- ✅ Data displays in frontend

---

## 🎉 You're Done!

Your Terabox downloader is now live with:
- ✅ Cookie-free API
- ✅ Beautiful frontend
- ✅ Full CORS support
- ✅ Auto-deployment

**Share your creation with the world!** 🚀

---

**Total Time:** 15-20 minutes
**Cost:** $0 (100% Free)
**Difficulty:** Easy (No coding required)
