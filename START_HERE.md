# 🚀 START HERE - Redis Cloud Setup

## ⚠️ Server Won't Start? Fix in 2 Steps!

The application is configured for your Redis Cloud but needs your password.

---

## Step 1: Update Password in main.py

Open `main.py` and find **line 43**:

```python
REDIS_CLOUD_URL = "redis://default:YOUR_PASSWORD_HERE@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

**Replace `YOUR_PASSWORD_HERE` with your actual Redis password.**

Example:
```python
REDIS_CLOUD_URL = "redis://default:abc123XYZ@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

Get your password from: https://app.redislabs.com

---

## Step 2: Run the Server

```bash
pip install -r requirements.txt
python main.py
```

---

## ✅ Success Looks Like:

```
INFO: Attempting to connect to Redis...
INFO: ✓ Redis connected successfully: redis://default:****@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
INFO: Uvicorn running on http://0.0.0.0:8000
```

**No more localhost:6379 errors!**

---

## Alternative: Use Environment Variable (Don't Edit File)

If you prefer not to edit the file:

```bash
export REDIS_URL="redis://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
python main.py
```

**Windows:**
```powershell
$env:REDIS_URL="redis://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
python main.py
```

---

## 🔧 Quick Test Redis Connection

Before running the app, test if your password works:

```bash
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD
```

Should respond with `PONG` when you type `PING`.

---

## 🚫 Disable Redis (Run Without Cache)

If you want to run without Redis temporarily:

```bash
export ENABLE_REDIS=false
python main.py
```

Server will start immediately with no caching.

---

**That's it! Update the password and run.** 🎉
