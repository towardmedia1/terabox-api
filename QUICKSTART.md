# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites
- Python 3.11+
- Redis 7.0+ (optional - can be disabled for local testing, or use Redis Cloud)
- pip

### Option 1: Local Development WITHOUT Redis (Fastest - No Setup!)

```bash
# 1. Disable Redis caching (for local testing)
export ENABLE_REDIS=false

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

**Service will be available at:** `http://localhost:8000`

**Note:** This mode works perfectly for testing but responses will be slower (no caching).
See `NO_REDIS_SETUP.md` for details.

### Option 2: Local Development WITH Redis Cloud (Recommended - No Local Redis Needed!)

```bash
# 1. Set your Redis Cloud URL (replace YOUR_PASSWORD)
export REDIS_URL="rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

**Service will be available at:** `http://localhost:8000`

**Note:** See `REDIS_CLOUD_SETUP.md` for detailed Redis Cloud configuration.

### Option 3: Local Development WITH Local Redis

```bash
# 1. Install Redis (if not already installed)
# Ubuntu/Debian:
sudo apt-get install redis-server
# macOS:
brew install redis
# Windows: Download from https://redis.io/download

# 2. Start Redis
redis-server

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

**Service will be available at:** `http://localhost:8000`

### Option 4: Docker Compose (Complete Stack with Redis)

```bash
# 1. Start everything with one command
docker-compose up -d

# 2. Check status
docker-compose ps

# 3. View logs
docker-compose logs -f app
```

**Service will be available at:** `http://localhost:8000`

---

## 🧪 Test the API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "redis": "connected",
  "http_client": "initialized"
}
```

### 2. Test Resolution Endpoint

**Update API Key First:**
Open `main.py` and find this section:
```python
VALID_API_KEYS = {
    "sk_prod_example_key_replace_in_production",
    "sk_test_another_valid_key_replace_in_production"
}
```

**Make a Test Request:**
```bash
curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{
    "url": "https://terabox.com/s/1234567890?surl=abc123&other=params",
    "ndus_token": "optional_auth_token"
  }'
```

### 3. Run Automated Test Suite

```bash
# Make sure the server is running first
python test_api.py
```

---

## 📖 API Documentation

Once running, visit:
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env`:
```bash
# API Keys (comma-separated)
API_KEYS=your_secure_key_here,another_key_here

# Redis
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=3600

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10

# Server
PORT=8000
LOG_LEVEL=info
```

### Update API Keys in Code

For quick testing, edit `main.py`:

```python
# Line ~55-58
VALID_API_KEYS = {
    "your_custom_key_here",
    "another_key_here"
}
```

For production, load from environment:
```python
import os

VALID_API_KEYS = set(os.getenv("API_KEYS", "").split(","))
```

---

## 🎯 Common Use Cases

### 1. Basic Resolution (No Authentication)
```bash
curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{"url": "https://terabox.com/s/file?surl=xyz123"}'
```

### 2. With Authentication Token
```bash
curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{
    "url": "https://terabox.com/s/file?surl=xyz123",
    "ndus_token": "your_ndus_cookie_value"
  }'
```

### 3. Check Cache Performance
```bash
# First request (cache miss)
time curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{"url": "https://terabox.com/s/file?surl=xyz123"}'

# Second request (cache hit - should be much faster)
time curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{"url": "https://terabox.com/s/file?surl=xyz123"}'
```

### 4. Python Client Example
```python
import httpx
import asyncio

async def resolve_url(url: str, api_key: str, ndus_token: str = None):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/resolve",
            json={"url": url, "ndus_token": ndus_token},
            headers={"X-API-Key": api_key}
        )
        return response.json()

# Usage
result = asyncio.run(resolve_url(
    url="https://terabox.com/s/file?surl=xyz123",
    api_key="sk_prod_example_key_replace_in_production",
    ndus_token="optional_token"
))

print(f"Direct Link: {result['direct_link']}")
print(f"Cached: {result['cached']}")
```

---

## 🛠️ Troubleshooting

### Issue: "Connection refused" when starting

**Solution:**
```bash
# Check if Redis is running
redis-cli ping
# Should respond with "PONG"

# If not running, start Redis
redis-server
```

### Issue: "Redis connection failed"

**Solution:**
```bash
# Check Redis URL in main.py (line ~237)
redis://localhost:6379/0

# Or set environment variable
export REDIS_URL=redis://localhost:6379/0
```

### Issue: 403 Forbidden

**Solution:** Check your API key
```bash
# Verify you're using a valid key from VALID_API_KEYS in main.py
# Default test key: sk_prod_example_key_replace_in_production
```

### Issue: 400 "Unable to extract surl parameter"

**Solution:** Ensure your URL contains the `surl` parameter
```bash
# ✗ Wrong
https://terabox.com/s/file

# ✓ Correct
https://terabox.com/s/file?surl=abc123
```

### Issue: 502 Bad Gateway

**Possible causes:**
1. Invalid `surl` parameter (doesn't exist on terabox.com)
2. Gateway returned error (check `errno` in logs)
3. Network connectivity issues to terabox.com

**Debug:**
```bash
# Check application logs
docker-compose logs -f app

# Or if running locally, check console output
```

### Issue: Rate limit (429)

**Solution:** Wait 60 seconds or adjust rate limit
```python
# In main.py, line ~373
RATE_LIMIT = "10/minute"  # Change to "100/minute" for testing
```

---

## 📦 Project Structure

```
url-resolver/
├── main.py                 # Core application (full implementation)
├── requirements.txt        # Python dependencies
├── test_api.py            # Automated test suite
├── .env.example           # Configuration template
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Multi-service orchestration
├── Makefile              # Convenience commands
├── README.md             # Comprehensive documentation
├── ARCHITECTURE.md       # Technical architecture details
├── QUICKSTART.md         # This file
└── deploy/
    ├── systemd/
    │   └── url-resolver.service    # Systemd service
    ├── nginx/
    │   └── url-resolver.conf       # Nginx reverse proxy
    └── scripts/
        └── deploy.sh               # Production deployment
```

---

## ⚡ Makefile Commands (Optional)

If you have `make` installed:

```bash
# Development
make install         # Install dependencies
make dev            # Run with auto-reload
make test           # Run test suite

# Docker
make docker-up      # Start services
make docker-down    # Stop services
make docker-logs    # View logs

# Maintenance
make clean          # Clean temporary files
make check-redis    # Verify Redis connection
make health         # Quick health check
```

---

## 🎓 Next Steps

1. **Read the full README.md** for comprehensive documentation
2. **Review ARCHITECTURE.md** for technical deep-dive
3. **Customize API keys** for your environment
4. **Set up monitoring** (see README.md monitoring section)
5. **Deploy to production** (see deployment guide in README.md)

---

## 💡 Quick Tips

✅ **Cache is working if:** Second identical request returns `"cached": true`

✅ **Rate limiting is working if:** 11th request in a minute returns HTTP 429

✅ **Authentication is working if:** Request without X-API-Key returns HTTP 403

✅ **Resolution is working if:** Valid surl returns HTTP 200 with `direct_link`

---

## 🆘 Need Help?

- **Application Logs:** Check console output or `docker-compose logs -f app`
- **Redis Logs:** `docker-compose logs -f redis`
- **Health Status:** `curl http://localhost:8000/health`
- **API Docs:** http://localhost:8000/docs (interactive testing)

---

## 🔐 Security Checklist (Before Production)

- [ ] Replace default API keys with secure random values
- [ ] Set up environment variables (don't hardcode secrets)
- [ ] Enable HTTPS/TLS (use Nginx with SSL certificate)
- [ ] Configure Redis authentication (`requirepass`)
- [ ] Set up firewall rules (only allow necessary ports)
- [ ] Enable logging and monitoring
- [ ] Set up backup strategy for Redis
- [ ] Review and adjust rate limits
- [ ] Implement API key rotation mechanism
- [ ] Set up alerting for errors and downtime

---

**You're all set! 🎉** The service should now be running at http://localhost:8000
