# Redis Cloud Configuration Guide

## 🌐 Connecting to Redis Cloud

Your Redis Cloud instance: `everlasting-kittenish-sneeze-82380.db.redis.io:12512`

---

## 🚀 Quick Setup

### Option 1: Environment Variable (Recommended)

```bash
# Set the Redis URL with authentication
export REDIS_URL="redis://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"

# Or with SSL/TLS (recommended for production)
export REDIS_URL="rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"

# Run the application
python main.py
```

**Important:** Replace `YOUR_PASSWORD` with your actual Redis Cloud password.

### Option 2: .env File (Recommended for Development)

Create a `.env` file:

```bash
# .env
ENABLE_REDIS=true

# Without SSL (development)
REDIS_URL=redis://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0

# With SSL (production)
# REDIS_URL=rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0

REDIS_MAX_CONNECTIONS=50
CACHE_TTL_SECONDS=3600
```

Then run:
```bash
python main.py
```

### Option 3: Docker with Redis Cloud

Update your `docker-compose.yml` to remove the local Redis service and use Redis Cloud:

```yaml
version: '3.8'

services:
  # Remove the redis service, use Redis Cloud instead
  
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: url_resolver_api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
      - CACHE_TTL_SECONDS=3600
      - RATE_LIMIT_PER_MINUTE=10
      - LOG_LEVEL=info
    networks:
      - resolver_network

networks:
  resolver_network:
    driver: bridge
```

Then:
```bash
docker-compose up -d
```

---

## 🔐 Redis URL Formats

### Basic Format (No SSL)
```
redis://[username]:[password]@[host]:[port]/[database]
```

Example:
```
redis://default:mypassword123@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
```

### Secure Format (SSL/TLS) - Recommended
```
rediss://[username]:[password]@[host]:[port]/[database]
```

Example:
```
rediss://default:mypassword123@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
```

**Note:** Use `rediss://` (with double 's') for SSL/TLS connections.

---

## 📋 Your Redis Cloud Details

| Parameter | Value |
|-----------|-------|
| **Host** | `everlasting-kittenish-sneeze-82380.db.redis.io` |
| **Port** | `12512` |
| **Default Username** | `default` |
| **Password** | `[Get from Redis Cloud dashboard]` |
| **Database** | `0` (default) |
| **SSL/TLS** | Recommended (use `rediss://`) |

---

## 🔍 Finding Your Password

1. Log in to your Redis Cloud dashboard
2. Navigate to your database: `everlasting-kittenish-sneeze-82380`
3. Click on "Configuration" or "Security"
4. Copy the password (or generate a new one)

---

## ✅ Verification

### 1. Test Connection with redis-cli

```bash
# Without SSL
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD

# With SSL
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD --tls

# Test
> PING
PONG
```

### 2. Test with Python

```python
import redis

# Connect
r = redis.Redis(
    host='everlasting-kittenish-sneeze-82380.db.redis.io',
    port=12512,
    password='YOUR_PASSWORD',
    ssl=True,  # For SSL/TLS
    decode_responses=True
)

# Test
print(r.ping())  # Should return True
```

### 3. Test with the Application

```bash
# Set Redis URL
export REDIS_URL="rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"

# Start application
python main.py
```

**Expected output:**
```
INFO: Initializing application resources...
INFO: Redis connection pool initialized successfully (URL: rediss://default:****@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0)
INFO: HTTP client initialized with connection pooling
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Check health:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "redis": "connected",
  "http_client": "initialized"
}
```

---

## 🔧 Configuration Options

### Environment Variables

```bash
# Required
export REDIS_URL="rediss://default:password@host:port/0"

# Optional
export REDIS_MAX_CONNECTIONS=50
export CACHE_TTL_SECONDS=3600
export ENABLE_REDIS=true
```

### .env File (Full Example)

```bash
# API Keys
API_KEYS=your_key_1,your_key_2

# Redis Cloud Configuration
ENABLE_REDIS=true
REDIS_URL=rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
REDIS_MAX_CONNECTIONS=50
CACHE_TTL_SECONDS=3600

# Gateway Configuration
INTERNAL_GATEWAY_URL=https://terabox.com
FIXED_APP_ID=250528

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10

# Server
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info
```

---

## 🔐 Security Best Practices

### 1. Never Commit Passwords

```bash
# Add to .gitignore (already included)
.env
.env.local
.env.production
```

### 2. Use SSL/TLS in Production

Always use `rediss://` (not `redis://`) for production:
```bash
# ✅ Good (SSL enabled)
rediss://default:password@host:port/0

# ❌ Bad (no encryption)
redis://default:password@host:port/0
```

### 3. Use Separate Passwords

Use different passwords for:
- Development
- Staging
- Production

### 4. Rotate Passwords Regularly

Change your Redis Cloud password every 90 days.

---

## 🚨 Troubleshooting

### Issue: "Connection refused"

**Solution:**
- Check if your IP is whitelisted in Redis Cloud dashboard
- Verify the host and port are correct
- Check firewall settings

### Issue: "Authentication failed"

**Solution:**
```bash
# Verify password is correct
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD --tls

# Make sure password is in URL
export REDIS_URL="rediss://default:YOUR_PASSWORD@host:port/0"
```

### Issue: "SSL certificate verify failed"

**Solution:**
The application is configured to not verify SSL certificates for Redis Cloud. If you still have issues:

```bash
# Try without SSL first to test
export REDIS_URL="redis://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
```

### Issue: "Too many connections"

**Solution:**
```bash
# Reduce max connections
export REDIS_MAX_CONNECTIONS=20
```

### Issue: Password visible in logs

**Solution:**
The application automatically masks passwords in logs. You should see:
```
INFO: Redis connection pool initialized successfully (URL: rediss://default:****@host:port/0)
```

---

## 📊 Performance with Redis Cloud

### Expected Latency

| Operation | Local Redis | Redis Cloud |
|-----------|-------------|-------------|
| Cache Write | 2-5ms | 10-30ms |
| Cache Read | 2-5ms | 10-30ms |
| Cache Miss → Gateway | 300-800ms | 300-800ms |

**Note:** Redis Cloud adds network latency but is still much faster than hitting the gateway every time.

### Throughput

With Redis Cloud, you can expect:
- **Cache Hit:** ~100-200 req/s per instance
- **Cache Miss:** ~50 req/s per instance
- **Mixed:** ~70-100 req/s per instance

---

## 🌍 Multi-Region Setup

If deploying to multiple regions, consider:

1. **Use Redis Cloud's multi-region support**
2. **Deploy Redis instances in each region**
3. **Use Active-Active for geo-replication**

---

## 💰 Redis Cloud Pricing Considerations

Monitor your usage:
- **Memory usage:** Each cached URL takes ~1-2KB
- **Connections:** Limit `REDIS_MAX_CONNECTIONS` appropriately
- **Operations:** Read/write operations count toward quota

Calculate needs:
```
Memory = (URLs cached) × (avg URL size + response size)
Example: 10,000 URLs × 2KB = 20MB
```

---

## 🔄 Switching Between Local and Cloud

### Use Local Redis (Development)
```bash
export REDIS_URL="redis://localhost:6379/0"
python main.py
```

### Use Redis Cloud (Production)
```bash
export REDIS_URL="rediss://default:password@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"
python main.py
```

### Disable Redis (Testing)
```bash
export ENABLE_REDIS=false
python main.py
```

---

## 📝 Example Configuration Files

### Development (.env.development)
```bash
ENABLE_REDIS=true
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=debug
```

### Staging (.env.staging)
```bash
ENABLE_REDIS=true
REDIS_URL=rediss://default:STAGING_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
LOG_LEVEL=info
```

### Production (.env.production)
```bash
ENABLE_REDIS=true
REDIS_URL=rediss://default:PRODUCTION_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0
REDIS_MAX_CONNECTIONS=50
CACHE_TTL_SECONDS=3600
LOG_LEVEL=warning
```

---

## ✅ Deployment Checklist

Before deploying with Redis Cloud:

- [ ] Obtain Redis Cloud password
- [ ] Update `.env` or set environment variable with Redis URL
- [ ] Use `rediss://` (SSL) for production
- [ ] Test connection with `redis-cli`
- [ ] Verify application connects successfully
- [ ] Check health endpoint shows "redis": "connected"
- [ ] Test cache hit/miss behavior
- [ ] Monitor memory usage in Redis Cloud dashboard
- [ ] Set up alerts for connection issues
- [ ] Document password in secure location (password manager)

---

## 🆘 Support

- **Redis Cloud Dashboard:** [https://app.redislabs.com](https://app.redislabs.com)
- **Redis Cloud Docs:** [https://docs.redis.com/latest/](https://docs.redis.com/latest/)
- **Application Logs:** Check console output or `docker-compose logs -f app`

---

**Quick Command Reference:**

```bash
# Set Redis Cloud URL
export REDIS_URL="rediss://default:YOUR_PASSWORD@everlasting-kittenish-sneeze-82380.db.redis.io:12512/0"

# Run application
python main.py

# Check health
curl http://localhost:8000/health

# Test Redis directly
redis-cli -h everlasting-kittenish-sneeze-82380.db.redis.io -p 12512 -a YOUR_PASSWORD --tls
```

---

**Status:** ✅ Redis Cloud Configuration Ready  
**Your Instance:** `everlasting-kittenish-sneeze-82380.db.redis.io:12512`  
**SSL/TLS:** Supported and Recommended
