# ☁️ Redis Cloud - Quick Start

## Your Redis Instance

```
Host: everlasting-kittenish-sneeze-82380.db.redis.io
Port: 12512
```

---

## 🚀 Get Running in 30 Seconds

### Step 1: Get Your Password

1. Go to [Redis Cloud Dashboard](https://app.redislabs.com)
2. Find your database: `everlasting-kittenish-sneeze-82380`
3. Copy the password

### Step 2: Set Environment Variable

```bash
# Replace YOUR_PASSWORD with actual password
export REDIS_URL="rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

**Windows PowerShell:**
```powershell
$env:REDIS_URL="rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

**Windows CMD:**
```cmd
set REDIS_URL=rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
```

### Step 3: Run the Application

```bash
pip install -r requirements.txt
python main.py
```

---

## ✅ Verify It's Working

### Check Console Output

You should see:
```
INFO: Redis connection pool initialized successfully (URL: rediss://default:****@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0)
```

### Check Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "redis": "connected",
  "http_client": "initialized"
}
```

### Test Caching

```bash
# First request (cache miss - slower)
time curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{"url": "https://terabox.com/s/file?surl=test123"}'

# Second request (cache hit - faster!)
time curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{"url": "https://terabox.com/s/file?surl=test123"}'
```

Second request should show `"cached": true` and be much faster!

---

## 🔧 Alternative: Using .env File

### Create .env file

```bash
# Copy template
cp .env.redis-cloud .env

# Edit with your password
nano .env  # or use any editor
```

### Update password in .env

```bash
REDIS_URL=rediss://default:YOUR_ACTUAL_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
```

### Run

```bash
python main.py
```

---

## 🚨 Troubleshooting

### "Connection refused"

**Check:**
1. Password is correct
2. IP is whitelisted in Redis Cloud dashboard
3. Using correct port (12512)

**Fix:**
```bash
# Test connection directly
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD --tls
```

### "SSL certificate verify failed"

**Fix:** Use `rediss://` (double s) for SSL:
```bash
export REDIS_URL="rediss://default:PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

### Password visible in error messages

**No worry!** The application automatically masks passwords in logs:
```
rediss://default:****@host:port/0
```

---

## 📋 Quick Reference

### Environment Variable Format

```bash
# With SSL (recommended)
rediss://default:PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0

# Without SSL (not recommended)
redis://default:PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
```

### Test Commands

```bash
# Test Redis connection
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD --tls

# Start application
python main.py

# Check health
curl http://localhost:8000/health

# Test API
curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{"url": "https://terabox.com/s/file?surl=test"}'
```

---

## 💡 Pro Tips

1. **Use SSL/TLS:** Always use `rediss://` (not `redis://`) for production
2. **Keep Password Secret:** Never commit `.env` to git (already in .gitignore)
3. **Monitor Usage:** Check Redis Cloud dashboard for memory and operations
4. **Set TTL:** Default is 3600s (1 hour) - adjust with `CACHE_TTL_SECONDS`
5. **Connection Pool:** Default is 50 connections - adjust with `REDIS_MAX_CONNECTIONS`

---

## 🎯 What You Get

✅ **Fast Caching** - 10-30ms cache hits (vs 300-800ms gateway hits)  
✅ **No Local Redis Needed** - Cloud-hosted, managed service  
✅ **Automatic Failover** - Redis Cloud handles redundancy  
✅ **Easy Scaling** - Upgrade plan in Redis Cloud dashboard  
✅ **Secure** - SSL/TLS encryption built-in  

---

## 📚 More Information

- **Detailed Guide:** See `REDIS_CLOUD_SETUP.md`
- **Alternative: Local Redis:** See `QUICKSTART.md`
- **No Redis Mode:** See `NO_REDIS_SETUP.md`

---

**Your Redis Instance:** `everlasting-kittenish-sneeze-82380.db.redis.io:12512`  
**Status:** ✅ Ready to Use  
**Setup Time:** ~30 seconds
