# URL Resolution Engine - Production Microservice

A high-performance, production-ready FastAPI microservice for resolving internal URLs in a distributed token-gated storage platform. Features comprehensive caching, rate limiting, API key authentication, and robust error handling.

## Architecture Overview

### Core Components

1. **Resolution Layer**: Async URL parameter extraction and internal gateway communication
2. **Security Layer**: API key authentication with FastAPI Security dependencies
3. **Performance Layer**: Redis-backed caching with connection pooling (3600s TTL)
4. **Rate Limiting**: IP-based throttling (10 requests/minute via SlowAPI)
5. **Error Handling**: Structured exception handling with standardized JSON responses

## Features

- ✅ Asynchronous request handling with connection pooling
- ✅ Redis caching with automatic TTL management
- ✅ API key authentication (X-API-Key header)
- ✅ IP-based rate limiting (configurable)
- ✅ Comprehensive error handling and logging
- ✅ Production-ready Docker containerization
- ✅ Health check endpoints
- ✅ Stateless architecture for horizontal scaling

## Requirements

- Python 3.11+
- Redis 7.0+
- Docker (optional, for containerized deployment)

## Installation

### Local Development

1. **Clone and setup**:
```bash
pip install -r requirements.txt
```

2. **Configure Redis** (optional for local testing):

   **Option A: Run WITHOUT Redis (Quick Testing)**
   ```bash
   export ENABLE_REDIS=false
   python main.py
   ```
   Perfect for quick testing without Redis installation. See `NO_REDIS_SETUP.md` for details.

   **Option B: Run WITH Redis (Production-like)**
   ```bash
   # Start Redis
   redis-server
   
   # Run application (Redis enabled by default)
   python main.py
   ```

3. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the application**:
```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python main.py
```

### Docker Deployment

1. **Using Docker Compose** (recommended):
```bash
docker-compose up -d
```

2. **Manual Docker build**:
```bash
# Build image
docker build -t url-resolver:latest .

# Run with external Redis
docker run -d \
  -p 8000:8000 \
  -e REDIS_URL=redis://your-redis-host:6379/0 \
  --name url-resolver \
  url-resolver:latest
```

## API Documentation

### Authentication

All requests to `/api/v1/resolve` require the `X-API-Key` header:

```bash
X-API-Key: sk_prod_example_key_replace_in_production
```

### Endpoints

#### POST `/api/v1/resolve`

Resolve internal URL to direct download link.

**Request Body**:
```json
{
  "url": "https://example.com/share?surl=abcd1234&extra=params",
  "ndus_token": "optional_authentication_token"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "direct_link": "https://resolved-download-link.com/file.zip",
  "cached": false,
  "source_url": "https://example.com/share?surl=abcd1234&extra=params"
}
```

**Error Response** (4xx/5xx):
```json
{
  "success": false,
  "error": "Error description",
  "error_code": "HTTP_400",
  "trace_id": "optional-trace-id"
}
```

#### GET `/health`

Health check with dependency status.

**Response**:
```json
{
  "status": "healthy",
  "redis": "connected",
  "http_client": "initialized"
}
```

## Usage Examples

### cURL

```bash
curl -X POST http://localhost:8000/api/v1/resolve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk_prod_example_key_replace_in_production" \
  -d '{
    "url": "https://terabox.com/s/1abcd1234567890?surl=xyz123",
    "ndus_token": "your_auth_token_here"
  }'
```

### Python

```python
import httpx

async def resolve_url(source_url: str, api_key: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/resolve",
            json={"url": source_url},
            headers={"X-API-Key": api_key}
        )
        return response.json()
```

### JavaScript/TypeScript

```typescript
const response = await fetch('http://localhost:8000/api/v1/resolve', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'sk_prod_example_key_replace_in_production'
  },
  body: JSON.stringify({
    url: 'https://terabox.com/s/1abcd1234567890?surl=xyz123',
    ndus_token: 'optional_token'
  })
});

const data = await response.json();
console.log(data.direct_link);
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `CACHE_TTL_SECONDS` | `3600` | Cache expiration time |
| `RATE_LIMIT_PER_MINUTE` | `10` | Requests per minute per IP |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `LOG_LEVEL` | `info` | Logging level |

### API Key Management

Update `VALID_API_KEYS` in `main.py` or load from environment:

```python
import os

VALID_API_KEYS = set(os.getenv("API_KEYS", "").split(","))
```

## Performance Optimization

### Connection Pooling

- **HTTP Client**: 100 max connections, 20 keepalive
- **Redis**: 50 max connections with keepalive
- **HTTP/2**: Enabled for multiplexing

### Caching Strategy

- **Cache Key**: `resolve:{source_url}`
- **TTL**: 3600 seconds (1 hour)
- **Policy**: Write-through caching
- **Eviction**: Automatic via TTL

### Rate Limiting

- **Strategy**: IP-based sliding window
- **Limit**: 10 requests/minute (configurable)
- **Response**: HTTP 429 with Retry-After header

## Production Deployment

### Scaling Recommendations

1. **Horizontal Scaling**: Deploy multiple instances behind load balancer
2. **Redis**: Use Redis Cluster or managed service (AWS ElastiCache, Redis Cloud)
3. **Workers**: Set workers to `2 × CPU cores`
4. **Resources**: Minimum 512MB RAM, 0.5 CPU per instance

### Production Checklist

- [ ] Replace default API keys with secure random values
- [ ] Configure Redis with persistence (AOF + RDB)
- [ ] Set up SSL/TLS termination at load balancer
- [ ] Enable structured logging (JSON format)
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Set up alerting for error rates and latency
- [ ] Implement request tracing (OpenTelemetry)
- [ ] Regular security updates and dependency scanning

### VPS Deployment (Systemd)

Create `/etc/systemd/system/url-resolver.service`:

```ini
[Unit]
Description=URL Resolution Engine
After=network.target redis.service

[Service]
Type=notify
User=appuser
WorkingDirectory=/opt/url-resolver
Environment="PATH=/opt/url-resolver/venv/bin"
ExecStart=/opt/url-resolver/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable url-resolver
sudo systemctl start url-resolver
```

## Monitoring

### Metrics to Track

- Request rate (requests/second)
- Cache hit rate (%)
- P50/P95/P99 latency
- Error rate by status code
- Redis connection pool utilization
- Rate limit violations

### Logging

Structured logs include:
- Request/response timing
- Cache hit/miss events
- Authentication failures
- Rate limit events
- Gateway errors with context

## Security Considerations

1. **API Keys**: Store in secure secret manager (AWS Secrets Manager, HashiCorp Vault)
2. **Rate Limiting**: Prevents abuse and DDoS
3. **Input Validation**: Pydantic models with strict validation
4. **Error Messages**: No sensitive data in error responses
5. **HTTPS**: Always use TLS in production
6. **CORS**: Configure restrictive CORS policies

## Troubleshooting

### Redis Connection Issues

```bash
# Test Redis connectivity
redis-cli ping

# Check Redis logs
docker logs url_resolver_redis
```

### High Latency

1. Check Redis connection pool saturation
2. Monitor internal gateway response times
3. Verify network connectivity to terabox.com
4. Review cache hit rate

### Rate Limit Errors

- Adjust `RATE_LIMIT_PER_MINUTE` environment variable
- Implement user-based limits instead of IP-based
- Use Redis for distributed rate limiting

## License

Proprietary - Internal Use Only

## Support

For issues or questions, contact the backend architecture team.
