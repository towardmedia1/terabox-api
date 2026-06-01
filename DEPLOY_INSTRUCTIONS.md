# 🚀 Quick Deploy Instructions

## ✅ CORS is Already Configured!

Your `api_server.py` already has CORS middleware enabled:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ✅ All origins allowed
    allow_credentials=True,    # ✅ Credentials allowed
    allow_methods=["*"],       # ✅ All methods allowed
    allow_headers=["*"],       # ✅ All headers allowed
)
```

This means your frontend can fetch data without any CORS blocks! 🎉

---

## 📤 Deploy to GitHub & Render

### Option 1: Install Git (Recommended)

1. **Download Git:**
   - Go to: https://git-scm.com/download/win
   - Download and install Git for Windows

2. **Setup Repository (First Time Only):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Terabox downloader with CORS"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **Deploy Updates:**
   ```bash
   git add .
   git commit -m "Update: CORS enabled"
   git push origin main
   ```

   Or simply run:
   ```bash
   deploy.bat
   ```

### Option 2: GitHub Desktop (Easy)

1. **Download GitHub Desktop:**
   - https://desktop.github.com/

2. **Steps:**
   - Open GitHub Desktop
   - File → Add Local Repository
   - Select your project folder
   - Click "Publish repository"
   - Done! Auto-syncs to GitHub

### Option 3: Manual Upload (Quick)

1. **Go to GitHub:**
   - https://github.com/new
   - Create new repository

2. **Upload Files:**
   - Click "uploading an existing file"
   - Drag all project files
   - Commit changes

3. **Connect to Render:**
   - Render will auto-deploy on file changes

---

## 🔄 How Render Auto-Deploy Works

Once connected to GitHub:

1. **You push changes** → GitHub receives update
2. **GitHub notifies Render** → Webhook triggered
3. **Render rebuilds** → Runs `pip install -r requirements.txt`
4. **Render restarts** → New version live in 2-3 minutes

**No manual action needed on Render!** 🎯

---

## 🧪 Test CORS is Working

### Method 1: Browser Console

1. Open your frontend: `http://localhost:3000/index.html`
2. Open browser DevTools (F12)
3. Go to Console tab
4. Paste Terabox link and submit
5. Check Network tab - should see successful POST request
6. No CORS errors = ✅ Working!

### Method 2: Test Script

```bash
python test_api.py
```

Should return file data without errors.

### Method 3: Direct Test

```bash
curl -X POST http://localhost:8000/api/v1/fetch \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA\"}"
```

---

## 📋 Current Project Status

✅ **Backend (api_server.py)**
- CORS middleware configured
- All origins allowed
- All methods allowed
- All headers allowed
- Credentials enabled

✅ **Frontend (index.html)**
- Fetch API configured
- POST request to `/api/v1/fetch`
- JSON payload with `url` field
- Error handling included

✅ **Ready for Deployment**
- All files present
- Dependencies listed
- Procfile configured
- Documentation complete

---

## 🎯 Next Steps

1. **Install Git** (if not installed)
   - https://git-scm.com/download/win

2. **Create GitHub Repository**
   - https://github.com/new

3. **Push Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Terabox downloader with CORS"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

4. **Deploy to Render**
   - Go to https://dashboard.render.com
   - New → Web Service
   - Connect GitHub repository
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
   - Deploy!

5. **Update Frontend**
   - Get Render URL: `https://your-app.onrender.com`
   - Update `index.html` line 145:
     ```javascript
     const API_URL = 'https://your-app.onrender.com/api/v1/fetch';
     ```
   - Push changes to GitHub

6. **Deploy Frontend**
   - GitHub Pages / Netlify / Vercel
   - Upload `index.html`
   - Done!

---

## 🔍 Verify CORS Headers

After deployment, check CORS headers:

```bash
curl -I https://your-app.onrender.com/health
```

Should see:
```
access-control-allow-origin: *
access-control-allow-credentials: true
access-control-allow-methods: *
access-control-allow-headers: *
```

---

## 🐛 Troubleshooting

### "Git not recognized"
- Install Git: https://git-scm.com/download/win
- Restart terminal after installation

### "CORS error in browser"
- Check API is running
- Verify CORS middleware in code
- Check browser console for exact error
- Try different browser

### "Push rejected"
- Setup GitHub authentication
- Use GitHub Desktop (easier)
- Or use Personal Access Token

### "Render not updating"
- Check Render dashboard logs
- Verify GitHub webhook is connected
- Manual deploy: Render Dashboard → Manual Deploy

---

## 📞 Quick Help

**CORS Already Working?**
- Yes! ✅ Already configured in `api_server.py`

**Need to Update?**
- Just push to GitHub, Render auto-deploys

**No Git Installed?**
- Use GitHub Desktop (easier)
- Or manual upload to GitHub

**Render Not Connected?**
- Go to Render Dashboard
- Settings → GitHub
- Connect repository

---

## ✅ Summary

**Current Status:**
- ✅ CORS fully configured
- ✅ Frontend ready
- ✅ Backend ready
- ✅ All files present

**To Deploy:**
1. Install Git (or use GitHub Desktop)
2. Push to GitHub
3. Connect to Render
4. Update frontend API URL
5. Deploy frontend
6. Done! 🎉

---

**Your API is production-ready with full CORS support!** 🚀
