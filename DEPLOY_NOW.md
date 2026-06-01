# 🚀 DEPLOY NOW - Quick Guide

## ✅ Changes Are Ready!

The URL expansion logic has been fixed in `api_server.py`. Now you need to deploy.

---

## 🎯 Quick Deploy (Choose One):

### Option 1: GitHub Desktop (Easiest - 2 minutes)

1. **Download GitHub Desktop** (if not installed)
   - https://desktop.github.com

2. **Open GitHub Desktop**
   - File → Add Local Repository
   - Select your project folder

3. **Commit Changes**
   - You'll see `api_server.py` changed
   - Commit message: "Fix URL expansion for TeraBox links"
   - Click "Commit to main"

4. **Push**
   - Click "Push origin"
   - Done! ✅

---

### Option 2: Install Git & Push (5 minutes)

```bash
# Install Git
winget install Git.Git

# Restart PowerShell, then:
git add api_server.py
git commit -m "Fix URL expansion and parameter extraction for TeraBox links"
git push origin main
```

---

### Option 3: Manual Upload (3 minutes)

1. **Go to GitHub**
   - https://github.com/YOUR_USERNAME/YOUR_REPO

2. **Edit api_server.py**
   - Click on `api_server.py`
   - Click pencil icon (Edit)

3. **Copy & Paste**
   - Open your local `api_server.py`
   - Copy all content (Ctrl+A, Ctrl+C)
   - Paste in GitHub editor
   - Scroll down

4. **Commit**
   - Commit message: "Fix URL expansion for TeraBox links"
   - Click "Commit changes"

5. **Done!**
   - Render will auto-deploy in 2-3 minutes

---

## 🧪 Test Locally First (Recommended):

```bash
# Start server
python -m uvicorn api_server:app --reload --port 8000

# Open browser
http://localhost:8000

# Test with these URLs:
# - https://terabox.com/s/1xxxxx
# - https://1024tera.com/s/1xxxxx
```

---

## ✅ What Was Fixed:

- ✅ URL expansion now works properly
- ✅ Supports both terabox.com and 1024tera.com
- ✅ Better User-Agent headers
- ✅ Multiple fallback mechanisms
- ✅ Extracts uk and shareid reliably
- ✅ Graceful error handling

---

## 🎯 After Deployment:

1. **Wait 2-3 minutes** for Render to rebuild
2. **Check Render Dashboard** - Should show "Live"
3. **Test your deployed URL**
4. **Try different TeraBox links**

---

## 💡 Quick Test Commands:

```bash
# Test the endpoint
curl -X POST https://your-app.onrender.com/api/v1/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA"}'
```

---

## 🐛 If Still Getting Errors:

1. **Check Render Logs**
   - Dashboard → Your Service → Logs

2. **Verify Deployment**
   - Should see "Build successful"
   - Should see "Deploy live"

3. **Test Health Endpoint**
   ```
   https://your-app.onrender.com/health
   ```

---

**Choose a method above and deploy now!** 🚀

**Estimated time: 2-5 minutes**
