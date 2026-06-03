# Running Without Redis (Local Testing Mode)

## Quick Start - No Redis Required

The application now supports running **without Redis** for easy local testing and development.

### Option 1: Using Environment Variable (Recommended)

```bash
# Set environment variable to disable Redis
export ENABLE_REDIS=false

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

**On Windows (PowerShell):**
```powershell
$env:ENABLE_REDIS="false"
pip install -r requirements.txt
python main.py
```

**On Windows (CMD):**
```cmd
set ENABLE_REDIS=false
pip install -r requirements.txt
python main.py
```

### Option 2: Using .env File

Create a `.env` file in the project root:

```bash
# .env
ENABLE_REDIS=false
```

Then run:
```bash
pip install -r requirements.txt
python main.py
```

### Option 3: Direct Code Modification

Edit `main.py` and change line 32:

```python
# Change this line:
ENABLE_REDIS = os.getenv("ENABLE_REDIS", "true").lower() in ("true", "1", "yes")

# To this:
ENABLE_REDIS = False
```

Then run:
```bash
pip install -r requirements.txt
python main.py
```

---

## What Happens When Redis is Disabled?

### ✅ Still Works
- ✅ API endpoints function normally
- ✅ URL resolution works perfectly
- ✅ Authentication works
- ✅ Rate limiting works
- ✅ All validation works
- ✅ Error handling works

### ⚠️ Different Behavior
- ⚠️ **No caching** - Every request hits the live gateway
- ⚠️ **Slower responses** - Cache hits (~10ms) become cache misses (~300-800ms)
- ⚠️ **Higher gateway load** - All requests go to terabox.com
- ⚠️ Health check shows `"redis": "disabled"` instead of `"redis": "connected"`

---

## Verify It's Working

### 1. Start the Application

```bash
export ENABLE_REDIS=false
python main.py
```

**Expected Output:**
```
INFO:__main__:Initializing application resources...
WARNING:__main__:Redis caching is DISABLED - running in no-cache mode for local testing
INFO:__main__:HTTP client initialized with connection pooling
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2. Check Health Status

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "redis": "disabled",
  "http_client": "initialized"
}
```

### 3. Test the API

```bash
curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{
    "url": "https://terabox.com/s/1234567890?surl=test123&other=param"
  }'
```

**Expected Response (with test URL):**
```json
{
  "success": true,
  "direct_link": "https://resolved-link.com/file",
  "cached": false,
  "source_url": "https://terabox.com/s/1234567890?surl=test123&other=param"
}
```

Note: `"cached": false` will **always** be false when Redis is disabled.

---

## Testing Without Redis

The automated test suite still works:

```bash
export ENABLE_REDIS=false
python main.py &  # Start server in background
sleep 3           # Wait for server to start
python test_api.py
```

**Note:** The caching test will show `"cached": false` for all requests, which is expected behavior.

---

## Performance Comparison

### With Redis (Production)
```
First Request:  300-800ms  (cache miss, hits gateway)
Second Request: 10-15ms    (cache hit, instant return)
Third Request:  10-15ms    (cache hit, instant return)
...
```

### Without Redis (Local Testing)
```
First Request:  300-800ms  (hits gateway)
Second Request: 300-800ms  (hits gateway again)
Third Request:  300-800ms  (hits gateway again)
...
```

---

## When to Use Each Mode

### Use WITH Redis (ENABLE_REDIS=true)
- ✅ Production deployment
- ✅ Staging environments
- ✅ Performance testing
- ✅ Load testing
- ✅ When you have Redis installed

### Use WITHOUT Redis (ENABLE_REDIS=false)
- ✅ Quick local testing
- ✅ Development on machines without Redis
- ✅ CI/CD pipelines without Redis
- ✅ Debugging core logic (without cache interference)
- ✅ Testing gateway communication directly

---

## Re-enabling Redis Later

To re-enable Redis caching:

### Option 1: Environment Variable
```bash
export ENABLE_REDIS=true
python main.py
```

### Option 2: .env File
```bash
# .env
ENABLE_REDIS=true
REDIS_URL=redis://localhost:6379/0
```

### Option 3: Remove Environment Variable
```bash
unset ENABLE_REDIS  # Defaults to enabled
python main.py
```

Then ensure Redis is running:
```bash
# Start Redis
redis-server

# Verify it's running
redis-cli ping  # Should return "PONG"
```

---

## Troubleshooting

### Issue: Application still tries to connect to Redis

**Solution:** Make sure the environment variable is set **before** running:

```bash
# ✗ Wrong (environment variable not persisted)
ENABLE_REDIS=false
python main.py

# ✓ Correct (on same line)
ENABLE_REDIS=false python main.py

# ✓ Correct (exported)
export ENABLE_REDIS=false
python main.py
```

### Issue: Health check shows "redis": "disconnected"

This means Redis is **enabled** but not running. Either:

1. **Disable Redis:**
   ```bash
   export ENABLE_REDIS=false
   ```

2. **Start Redis:**
   ```bash
   redis-server
   ```

### Issue: Slower response times

This is **expected** when Redis is disabled. Every request hits the live gateway instead of returning cached results.

---

## Docker Without Redis

To run the Docker container without Redis:

```bash
# Build image
docker build -t url-resolver:latest .

# Run without Redis (standalone)
docker run -d \
  -p 8000:8000 \
  -e ENABLE_REDIS=false \
  --name url-resolver \
  url-resolver:latest
```

**Note:** This will run only the application container without the Redis container.

---

## Summary

✅ **Simple:** Just set `ENABLE_REDIS=false`  
✅ **Works Everywhere:** No Redis installation needed  
✅ **Full Functionality:** All features work except caching  
✅ **Easy Testing:** Perfect for quick development  
✅ **Reversible:** Re-enable anytime by setting `ENABLE_REDIS=true`  

**You can now run the application without Redis for easy local testing!** 🚀
