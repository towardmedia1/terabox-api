# 🚀 Heroku Deployment Guide

## ✅ Your API URL is Set to Heroku!

The `index.html` is now configured to use:
```javascript
const API_URL = 'https://herokuapp.com/api/v1/fetch';
```

**After deployment, replace `herokuapp.com` with your actual Heroku app URL!**

---

## 📦 Deploy to Heroku (3 Methods)

### Method 1: Heroku CLI (Recommended)

#### Step 1: Install Heroku CLI

**Windows:**
- Download: https://devcenter.heroku.com/articles/heroku-cli
- Or use: `winget install Heroku.HerokuCLI`

**Verify installation:**
```bash
heroku --version
```

#### Step 2: Login to Heroku

```bash
heroku login
```

This opens browser for authentication.

#### Step 3: Create Heroku App

```bash
# Create new app
heroku create your-app-name

# Or let Heroku generate name
heroku create
```

**Note your app URL:** `https://your-app-name.herokuapp.com`

#### Step 4: Deploy

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit: Terabox API"

# Add Heroku remote
heroku git:remote -a your-app-name

# Deploy
git push heroku main
```

#### Step 5: Verify Deployment

```bash
# Open app in browser
heroku open

# Check logs
heroku logs --tail

# Test health endpoint
curl https://your-app-name.herokuapp.com/health
```

---

### Method 2: GitHub Integration (Easy)

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Terabox API for Heroku"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

#### Step 2: Connect to Heroku

1. Go to https://dashboard.heroku.com
2. Click "New" → "Create new app"
3. App name: `your-app-name`
4. Region: Choose closest to you
5. Click "Create app"

#### Step 3: Deploy from GitHub

1. Go to "Deploy" tab
2. Deployment method: "GitHub"
3. Connect to GitHub
4. Search for your repository
5. Click "Connect"
6. Enable "Automatic deploys" (optional)
7. Click "Deploy Branch"

#### Step 4: Wait for Build

- Build takes 2-3 minutes
- Check build logs
- Once complete, click "View"

---

### Method 3: Manual Upload (No Git)

#### Step 1: Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

#### Step 2: Create App

```bash
heroku login
heroku create your-app-name
```

#### Step 3: Deploy Files

```bash
# Navigate to project folder
cd path/to/terbox-api

# Deploy
git init
git add .
git commit -m "Deploy to Heroku"
heroku git:remote -a your-app-name
git push heroku main
```

---

## 🔧 Heroku Configuration

### Required Files (Already Present)

✅ **`Procfile`** - Tells Heroku how to run app
```
web: uvicorn api_server:app --host 0.0.0.0 --port $PORT
```

✅ **`requirements.txt`** - Python dependencies
```
fastapi
uvicorn
httpx
```

✅ **`api_server.py`** - Main application

### Optional: Add runtime.txt

Specify Python version:

```bash
echo "python-3.11.0" > runtime.txt
git add runtime.txt
git commit -m "Add Python runtime"
git push heroku main
```

---

## 🔄 Update Frontend with Heroku URL

After deployment, update `index.html`:

### Step 1: Get Your Heroku URL

```bash
heroku info
```

Or check dashboard: `https://your-app-name.herokuapp.com`

### Step 2: Update index.html

**Find line 120:**
```javascript
const API_URL = 'https://herokuapp.com/api/v1/fetch';
```

**Replace with your actual URL:**
```javascript
const API_URL = 'https://your-app-name.herokuapp.com/api/v1/fetch';
```

### Step 3: Redeploy Frontend

**If using GitHub Pages:**
```bash
git add index.html
git commit -m "Update API URL"
git push origin main
```

**If using Netlify:**
- Re-upload `index.html`

---

## 🧪 Test Your Deployment

### Test API Health

```bash
curl https://your-app-name.herokuapp.com/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890,
  "version": "2.0.0"
}
```

### Test API Docs

Open in browser:
```
https://your-app-name.herokuapp.com/docs
```

### Test File Fetch

```bash
curl -X POST https://your-app-name.herokuapp.com/api/v1/fetch \
  -H "Content-Type: application/json" \
  -d '{"url":"https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA"}'
```

### Test Frontend

1. Open your frontend URL
2. Paste Terabox link
3. Click "Get Download Links"
4. Should see results!

---

## 📊 Heroku Dashboard

Access at: https://dashboard.heroku.com/apps/your-app-name

**Useful tabs:**
- **Overview** - App status, dyno usage
- **Resources** - Manage dynos
- **Deploy** - Deployment history
- **Logs** - View application logs
- **Settings** - Config vars, domains

---

## 🔍 View Logs

### Real-time logs:
```bash
heroku logs --tail
```

### Last 100 lines:
```bash
heroku logs -n 100
```

### Filter by source:
```bash
heroku logs --source app
```

---

## ⚙️ Environment Variables (Optional)

### Add config vars:

```bash
# Via CLI
heroku config:set COOKIE_POOL=cookie1,cookie2,cookie3

# Via Dashboard
# Settings → Config Vars → Reveal Config Vars → Add
```

### View config vars:
```bash
heroku config
```

---

## 🔄 Update Your App

### Deploy updates:

```bash
# Make changes to code
git add .
git commit -m "Update API"
git push heroku main
```

### Restart app:
```bash
heroku restart
```

### Scale dynos:
```bash
# Check current
heroku ps

# Scale up
heroku ps:scale web=1
```

---

## 💰 Heroku Pricing

### Free Tier (Eco Dynos)
- **Cost:** $5/month for 1000 dyno hours
- **Sleep:** After 30 min inactivity
- **Wake:** First request takes ~30s
- **Good for:** Testing, personal projects

### Hobby Tier
- **Cost:** $7/month
- **No sleep:** Always on
- **SSL:** Free SSL certificate
- **Good for:** Production apps

### Professional Tier
- **Cost:** $25+/month
- **Features:** Autoscaling, metrics
- **Good for:** High-traffic apps

---

## 🐛 Troubleshooting

### "Application Error"

**Check logs:**
```bash
heroku logs --tail
```

**Common causes:**
- Missing dependencies in `requirements.txt`
- Wrong Procfile command
- Port binding issue

**Fix:**
- Verify `Procfile` uses `$PORT`
- Check all dependencies listed
- Redeploy

### "Build Failed"

**Check build logs:**
```bash
heroku logs --tail
```

**Common causes:**
- Syntax error in code
- Missing `requirements.txt`
- Incompatible Python version

**Fix:**
- Test locally first
- Verify all files committed
- Check Python version compatibility

### "CORS Error"

**Already fixed!** ✅ CORS is configured in `api_server.py`

**If still seeing errors:**
- Verify API URL in `index.html` is correct
- Check API is running: `heroku ps`
- Test API directly with curl

### "App Sleeping"

**Free tier sleeps after 30 min inactivity**

**Solutions:**
1. Upgrade to Hobby tier ($7/month)
2. Use uptime monitor (pings app every 25 min)
3. Accept 30s wake-up time

---

## 🎯 Custom Domain (Optional)

### Add custom domain:

```bash
# Add domain
heroku domains:add www.yourdomain.com

# Get DNS target
heroku domains
```

### Update DNS:
- Add CNAME record pointing to Heroku DNS target
- Wait for DNS propagation (up to 48 hours)

---

## 📈 Monitoring

### Heroku Metrics (Dashboard)
- Response time
- Throughput
- Memory usage
- Error rate

### External Monitoring
- **UptimeRobot:** https://uptimerobot.com (free)
- **Pingdom:** https://pingdom.com
- **StatusCake:** https://statuscake.com

---

## 🔐 Security Best Practices

### 1. Use Environment Variables
```bash
heroku config:set SECRET_KEY=your-secret-key
```

### 2. Enable HTTPS (Automatic)
Heroku provides free SSL certificates

### 3. Add Rate Limiting
Install: `pip install slowapi`

### 4. Monitor Logs
```bash
heroku logs --tail
```

---

## ✅ Deployment Checklist

- [ ] Heroku CLI installed
- [ ] Logged into Heroku
- [ ] App created on Heroku
- [ ] Code pushed to Heroku
- [ ] Build successful
- [ ] App is running
- [ ] Health endpoint works
- [ ] API docs accessible
- [ ] Heroku URL copied
- [ ] `index.html` updated with URL
- [ ] Frontend redeployed
- [ ] Tested with real Terabox link
- [ ] Everything works! 🎉

---

## 🚀 Quick Commands Reference

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Restart app
heroku restart

# Open app
heroku open

# Check status
heroku ps

# View config
heroku config

# Add config var
heroku config:set KEY=value
```

---

## 📞 Need Help?

**Heroku Documentation:**
- https://devcenter.heroku.com/

**Heroku Support:**
- https://help.heroku.com/

**Check Status:**
- https://status.heroku.com/

---

## 🎉 Success!

Your Terabox API is now live on Heroku!

**Your URLs:**
- API: `https://your-app-name.herokuapp.com`
- Docs: `https://your-app-name.herokuapp.com/docs`
- Health: `https://your-app-name.herokuapp.com/health`

**Share your creation!** 🚀

---

**Deployment Time:** 10-15 minutes
**Cost:** $5-7/month (or free with limitations)
**Difficulty:** Easy
