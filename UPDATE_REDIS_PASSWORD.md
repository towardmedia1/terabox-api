# ⚠️ IMPORTANT: Update Redis Password

## 🔴 Required Action Before Running

The application is configured to use your Redis Cloud instance, but you need to **add your password**.

---

## 📝 Step 1: Get Your Redis Password

1. Go to [Redis Cloud Dashboard](https://app.redislabs.com)
2. Find your database: `everlasting-kittenish-sneeze-82380`
3. Copy the password

---

## ✏️ Step 2: Update main.py

### Option A: Edit main.py directly (Quick & Simple)

Open `main.py` and find **line 36**:

```python
REDIS_CLOUD_URL = "redis://default:YOUR_PASSWORD_HERE@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

Replace `YOUR_PASSWORD_HERE` with your actual password:

```python
REDIS_CLOUD_URL = "redis://default:myActualPassword123@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

**Save the file.**

### Option B: Use Environment Variable (Recommended for Security)

Instead of editing the file, set an environment variable:

```bash
export REDIS_URL="redis://default:YOUR_ACTUAL_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

**Windows PowerShell:**
```powershell
$env:REDIS_URL="redis://default:YOUR_ACTUAL_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

This way, your password isn't stored in the code file.

---

## 🚀 Step 3: Run the Application

```bash
python main.py
```

---

## ✅ Verify It's Working

You should see:
```
INFO: Attempting to connect to Redis...
INFO: ✓ Redis connected successfully: redis://default:****@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
INFO: HTTP client initialized with connection pooling
INFO: Uvicorn running on http://0.0.0.0:8000
```

**No more localhost:6379 errors!**

---

## 🚨 Troubleshooting

### If you see "Connection refused" or "Authentication failed"

**Check:**
1. Password is correct (no typos)
2. Password format: `redis://default:PASSWORD@host:port/0`
3. No extra spaces in the password

**Test connection:**
```bash
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD
```

Should return:
```
> PING
PONG
```

### If application still crashes

**Disable Redis temporarily to test:**
```bash
export ENABLE_REDIS=false
python main.py
```

This will run without Redis to verify other components work.

---

## 🔐 Security Note

**Don't commit your password to Git!**

If you edit main.py with your real password:
1. Don't commit that file
2. Consider using environment variables instead (Option B above)
3. Or use a `.env` file (already in .gitignore)

---

## 📋 Quick Reference

### Your Redis Details
- **Host:** `everlasting-kittenish-sneeze-82380.db.redis.io`
- **Port:** `12512`
- **Username:** `default`
- **Password:** `[Get from Redis Cloud]`

### Connection String Format
```
redis://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
```

### Where to Update
- **File:** `main.py`
- **Line:** ~36
- **Variable:** `REDIS_CLOUD_URL`

---

**After updating the password, the server will start successfully!** ✅
