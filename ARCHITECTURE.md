# URL Resolution Engine - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  (Mobile Apps, Web Frontend, Partner APIs, Internal Services)   │
└────────────────┬────────────────────────────────────────────────┘
                 │ HTTPS + X-API-Key
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Load Balancer / Nginx                         │
│  • SSL Termination         • Rate Limiting (20 req/min)         │
│  • Request Routing         • Connection Pooling                  │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                 FastAPI Application Layer                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          Security Middleware                             │  │
│  │  • API Key Validation (X-API-Key)                       │  │
│  │  • IP-based Rate Limiting (10 req/min via SlowAPI)      │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                            │
│  ┌──────────────────▼───────────────────────────────────────┐  │
│  │          Request Handler (/api/v1/resolve)              │  │
│  │  • Input Validation (Pydantic)                          │  │
│  │  • Request Logging                                       │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                            │
│          ┌──────────▼──────────┐                                │
│          │  Cache Lookup?      │                                │
│          └─────┬─────────┬─────┘                                │
│                │ Hit     │ Miss                                  │
│         ┌──────▼───┐    │                                       │
│         │  Redis   │    │                                       │
│         │  Cache   │    │                                       │
│         └──────┬───┘    │                                       │
│                │        │                                       │
│                │    ┌───▼────────────────────────────────────┐ │
│                │    │   Core Resolution Engine               │ │
│                │    │   • Extract 'surl' (Regex)             │ │
│                │    │   • Build Gateway Request              │ │
│                │    │   • HTTP Client (Connection Pool)      │ │
│                │    │   • Parse & Validate Response          │ │
│                │    │   • Extract 'dlink'                    │ │
│                │    └───┬────────────────────────────────────┘ │
│                │        │                                       │
│                │    ┌───▼────────────────────────────────────┐ │
│                │    │   Cache Write (TTL: 3600s)             │ │
│                │    └───┬────────────────────────────────────┘ │
│                └────────┼─────────────────────────────────────┐ │
│                         │                                      │ │
│  ┌──────────────────────▼──────────────────────────────────┐ │ │
│  │          Response Formatter                             │ │ │
│  │  • Build JSON Response                                  │ │ │
│  │  • Add Metadata (cached flag, source_url)              │ │ │
│  └─────────────────────────────────────────────────────────┘ │ │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  External Dependencies                           │
│                                                                   │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │   Redis Cache        │      │  Internal Gateway    │        │
│  │   • Port: 6379       │      │  terabox.com         │        │
│  │   • Connection Pool  │      │  • /share/list       │        │
│  │   • TTL: 3600s       │      │  • Authentication    │        │
│  │   • LRU Eviction     │      │  • JSON API          │        │
│  └──────────────────────┘      └──────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Core Resolution Layer

**File:** `main.py` - Functions: `extract_surl_parameter()`, `resolve_direct_link()`

**Responsibilities:**
- Parameter extraction using compiled regex (`SURL_PATTERN`)
- Gateway request construction with fixed parameters
- HTTP communication with connection pooling
- JSON response parsing and validation
- Business logic validation (`errno == 0`)
- Nested data extraction (`list[0]['dlink']`)

**Flow:**
```python
1. Extract 'surl' from URL → regex match
2. Build request: gateway_url + params (surl, root=1, app_id=250528)
3. Add authentication: ndus cookie token
4. Execute HTTP GET with httpx.AsyncClient
5. Parse JSON response
6. Validate errno == 0
7. Extract dlink from list[0]['dlink']
8. Return direct link string
```

**Error Handling:**
- 400: Missing surl parameter
- 502: Gateway errors (errno != 0, invalid response structure)
- 504: Timeout errors
- 500: Unexpected errors

---

### 2. Security Layer

**File:** `main.py` - Function: `verify_api_key()`

**Implementation:**
```python
Security: APIKeyHeader(name="X-API-Key")
Dependency: verify_api_key()
Storage: VALID_API_KEYS set
```

**Flow:**
```
Request → Extract X-API-Key Header → Validate against VALID_API_KEYS
   ↓                ↓                              ↓
Missing          Invalid                        Valid
   ↓                ↓                              ↓
 403             403                          Continue
```

**Production Considerations:**
- Load API keys from environment variables
- Use secret manager (AWS Secrets Manager, HashiCorp Vault)
- Implement key rotation mechanism
- Add API key usage tracking and analytics

---

### 3. Performance Layer (Caching)

**File:** `main.py` - Functions: `get_cached_link()`, `set_cached_link()`

**Redis Configuration:**
```python
Connection Pool: max_connections=50
Encoding: UTF-8
Decode Responses: True
Socket Keepalive: Enabled
```

**Cache Strategy:**
```
Cache Key Format: "resolve:{source_url}"
TTL: 3600 seconds (1 hour)
Eviction Policy: Automatic via TTL expiration

Flow:
┌─────────────┐
│   Request   │
└──────┬──────┘
       │
   ┌───▼────┐
   │ Redis  │ ──HIT──> Return Cached Result (cached=true)
   │ Lookup │
   └───┬────┘
       │ MISS
       ▼
┌─────────────┐
│  Execute    │
│ Resolution  │
└──────┬──────┘
       │
   ┌───▼────┐
   │ Cache  │
   │ Write  │
   └───┬────┘
       │
       ▼
  Return Result (cached=false)
```

**Performance Metrics:**
- Cache Hit Rate Target: >70%
- Cache Write Time: <5ms
- Cache Read Time: <2ms

---

### 4. Rate Limiting Layer

**File:** `main.py` - Implementation: SlowAPI

**Configuration:**
```python
Strategy: IP-based sliding window
Rate: 10 requests per minute
Identifier: get_remote_address (client IP)
Burst Allowance: Configurable in decorator
```

**Implementation:**
```python
@limiter.limit("10/minute")
async def resolve_url(request: Request, ...):
    ...
```

**Response on Limit Exceeded:**
```json
{
  "error": "Rate limit exceeded: 10 per 1 minute"
}
```
HTTP Status: 429 Too Many Requests
Header: Retry-After: <seconds>

**Advanced Scenarios:**
- Multi-tier limits (per IP, per API key, per user)
- Distributed rate limiting with Redis (for multi-instance)
- Whitelist for internal services
- Dynamic rate limits based on API key tier

---

### 5. Error Handling Architecture

**Structured Exception Hierarchy:**

```
Exception
├── HTTPException (FastAPI built-in)
│   ├── 400: Bad Request (validation, missing surl)
│   ├── 403: Forbidden (auth failures)
│   ├── 429: Too Many Requests (rate limit)
│   ├── 500: Internal Server Error
│   ├── 502: Bad Gateway (upstream errors)
│   └── 504: Gateway Timeout
│
└── Global Exception Handler
    └── Catches all unhandled exceptions
```

**Standardized Error Response:**
```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "HTTP_400 | INTERNAL_ERROR | GATEWAY_ERROR",
  "trace_id": "optional-request-id-for-tracing"
}
```

**Error Logging:**
- Level: ERROR for 5xx, WARNING for 4xx
- Context: Request ID, URL, API key (hashed), timestamp
- Structured logging with JSON formatter (production)

---

## Data Flow Diagram

### Successful Resolution (Cache Miss)

```
Client Request
    │
    ▼
[API Key Auth] ──✗──> 403 Forbidden
    │ ✓
    ▼
[Rate Limit Check] ──✗──> 429 Too Many Requests
    │ ✓
    ▼
[Input Validation] ──✗──> 422 Validation Error
    │ ✓
    ▼
[Redis Cache Lookup] ──HIT──> Return Cached Response
    │ MISS
    ▼
[Extract surl] ──✗──> 400 Bad Request (no surl)
    │ ✓
    ▼
[Build Gateway Request]
    │
    ▼
[HTTP GET to terabox.com]
    │
    ├──✗──> Timeout ──> 504 Gateway Timeout
    │
    ├──✗──> HTTP Error ──> 502 Bad Gateway
    │
    ▼ ✓
[Parse JSON Response]
    │
    ├──✗──> Invalid JSON ──> 502 Bad Gateway
    │
    ▼ ✓
[Validate errno == 0] ──✗──> 502 Gateway Error (errno != 0)
    │ ✓
    ▼
[Extract list[0]['dlink']] ──✗──> 502 Bad Gateway (missing dlink)
    │ ✓
    ▼
[Cache Write to Redis]
    │
    ▼
[Build Response]
    │
    ▼
200 OK + Direct Link
```

---

## Deployment Architecture

### Single Instance (VPS/VM)

```
┌─────────────────────────────────────────┐
│          VPS / Virtual Machine           │
│                                           │
│  ┌────────────────────────────────────┐ │
│  │  Nginx (Port 80/443)               │ │
│  │  • SSL Termination                 │ │
│  │  • Rate Limiting                   │ │
│  │  • Load Balancing (optional)       │ │
│  └────────┬───────────────────────────┘ │
│           │                               │
│  ┌────────▼───────────────────────────┐ │
│  │  FastAPI (Port 8000)               │ │
│  │  • Uvicorn Workers: 4              │ │
│  │  • Systemd Service                 │ │
│  └────────┬───────────────────────────┘ │
│           │                               │
│  ┌────────▼───────────────────────────┐ │
│  │  Redis (Port 6379)                 │ │
│  │  • Persistence: AOF + RDB          │ │
│  │  • Max Memory: 512MB               │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Multi-Instance (High Availability)

```
                   ┌─────────────┐
                   │   Clients   │
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │ Load Balancer│
                   │ (Nginx/HAProxy)│
                   └──────┬──────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                  │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │Instance1│      │Instance2│      │Instance3│
   │FastAPI  │      │FastAPI  │      │FastAPI  │
   │Port 8000│      │Port 8000│      │Port 8000│
   └────┬────┘      └────┬────┘      └────┬────┘
        │                 │                  │
        └─────────────────┼──────────────────┘
                          │
                   ┌──────▼──────┐
                   │Redis Cluster│
                   │   (3 nodes) │
                   └─────────────┘
```

### Docker/Kubernetes Deployment

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster               │
│                                           │
│  ┌────────────────────────────────────┐ │
│  │  Ingress Controller                │ │
│  │  (nginx-ingress / Traefik)         │ │
│  └────────┬───────────────────────────┘ │
│           │                               │
│  ┌────────▼───────────────────────────┐ │
│  │  Service: url-resolver             │ │
│  │  Type: ClusterIP                   │ │
│  └────────┬───────────────────────────┘ │
│           │                               │
│  ┌────────▼───────────────────────────┐ │
│  │  Deployment: url-resolver-api      │ │
│  │  Replicas: 3                       │ │
│  │  ┌──────────┐  ┌──────────┐       │ │
│  │  │  Pod 1   │  │  Pod 2   │  ...  │ │
│  │  │FastAPI   │  │FastAPI   │       │ │
│  │  └──────────┘  └──────────┘       │ │
│  └────────┬───────────────────────────┘ │
│           │                               │
│  ┌────────▼───────────────────────────┐ │
│  │  StatefulSet: redis                │ │
│  │  Replicas: 1 (or Redis Sentinel)  │ │
│  │  PVC: 10GB                         │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## Security Architecture

### Defense in Depth

**Layer 1: Network Security**
- Firewall rules (only ports 80/443 exposed)
- DDoS protection (Cloudflare, AWS Shield)
- VPC isolation (private subnets for backend)

**Layer 2: Transport Security**
- TLS 1.2+ only
- Strong cipher suites
- Certificate pinning (optional)

**Layer 3: Application Security**
- API key authentication
- IP-based rate limiting
- Input validation (Pydantic)
- Output encoding (JSON)

**Layer 4: Data Security**
- Redis authentication (requirepass)
- No sensitive data in logs
- Encrypted environment variables

**Layer 5: Infrastructure Security**
- Container image scanning
- Dependency vulnerability scanning
- Regular security patches
- Least privilege (non-root user)

### Threat Model

| Threat | Mitigation |
|--------|------------|
| API key theft | Key rotation, short-lived tokens, monitoring |
| DDoS attacks | Rate limiting, CDN, autoscaling |
| Injection attacks | Pydantic validation, parameterized queries |
| Data exposure | No logging of sensitive data, HTTPS only |
| Man-in-the-middle | TLS 1.2+, certificate validation |
| Cache poisoning | Input validation, TTL expiration |

---

## Performance Characteristics

### Latency Breakdown (Average)

```
Total Request Latency: ~300-800ms

┌─ API Key Validation: 1-2ms
├─ Rate Limit Check: 1-3ms
├─ Input Validation: 1-2ms
├─ Redis Lookup: 2-5ms
│  └─ Cache Hit: Return immediately (~10ms total)
│
├─ Cache Miss Path:
│  ├─ Regex Extraction: <1ms
│  ├─ Gateway Request: 200-500ms (network)
│  ├─ JSON Parsing: 2-5ms
│  ├─ Validation: 1-2ms
│  ├─ Redis Write: 3-5ms
│  └─ Response Building: 1-2ms
│
└─ Total (Cache Miss): ~300-800ms
   Total (Cache Hit): ~10-15ms
```

### Throughput

**Single Instance (4 workers):**
- Theoretical Max: ~400 req/s (cached)
- Practical Max: ~50 req/s (mixed cache hit/miss)
- With Rate Limiting: 10 req/min per IP

**Multi-Instance (3 instances × 4 workers):**
- Theoretical Max: ~1200 req/s (cached)
- Practical Max: ~150 req/s (mixed)

### Resource Usage

**Per Instance:**
- CPU: 0.5-2.0 cores (under load)
- Memory: 512MB-1GB
- Network: 10-50 Mbps

**Redis:**
- Memory: 256MB-1GB (depends on cache size)
- CPU: <0.1 cores
- Network: 5-10 Mbps

---

## Monitoring & Observability

### Key Metrics

**Application Metrics:**
- Request rate (requests/second)
- Error rate (errors/second, by status code)
- Latency (P50, P95, P99)
- Cache hit rate (%)
- Rate limit violations (count)

**Infrastructure Metrics:**
- CPU utilization (%)
- Memory utilization (%)
- Network I/O (Mbps)
- Disk I/O (for Redis persistence)

**Business Metrics:**
- Successful resolutions (count)
- Failed resolutions (count, by reason)
- Unique URLs resolved (count)
- API key usage (by key)

### Alerting Rules

| Alert | Condition | Severity |
|-------|-----------|----------|
| High Error Rate | Error rate > 10% for 5 min | Critical |
| High Latency | P95 > 2000ms for 5 min | Warning |
| Redis Down | Redis connection failed | Critical |
| Low Cache Hit | Hit rate < 50% for 10 min | Warning |
| High Memory | Memory > 90% for 5 min | Warning |
| Service Down | Health check failed 3x | Critical |

### Log Aggregation

**Log Levels:**
- ERROR: Application errors, gateway errors
- WARNING: Auth failures, rate limits, validation errors
- INFO: Request logging, cache events, service lifecycle
- DEBUG: Detailed execution traces (dev only)

**Log Format (Production):**
```json
{
  "timestamp": "2026-06-03T10:30:00Z",
  "level": "INFO",
  "message": "URL resolution successful",
  "request_id": "abc123",
  "api_key_hash": "sha256:...",
  "source_url_hash": "sha256:...",
  "cached": false,
  "latency_ms": 350,
  "gateway_status": 200
}
```

---

## Testing Strategy

### Unit Tests
- Regex extraction logic
- JSON parsing and validation
- Cache read/write operations
- Error handling paths

### Integration Tests
- End-to-end resolution flow
- Redis caching behavior
- Rate limiting enforcement
- API key authentication

### Load Tests
- Throughput testing (Apache JMeter, Locust)
- Stress testing (gradual load increase)
- Spike testing (sudden load spike)
- Endurance testing (sustained load)

### Security Tests
- Authentication bypass attempts
- Rate limit evasion attempts
- Injection attack vectors
- Fuzzing input validation

---

## Disaster Recovery

### Backup Strategy
- Redis snapshots every 6 hours
- Application configuration in version control
- Infrastructure as Code (Terraform/CloudFormation)

### Recovery Procedures

**Redis Failure:**
1. Service continues with degraded performance (no cache)
2. Monitor error rate for Redis connection failures
3. Restore Redis from latest snapshot or restart service
4. Cache rebuilds automatically on requests

**Application Failure:**
1. Systemd auto-restart (3 attempts)
2. Health check alerts on-call engineer
3. Rollback to previous version if recent deployment
4. Investigate logs and metrics

**Complete Outage:**
1. DNS failover to backup region (if multi-region)
2. Scale up backup instances
3. Restore Redis from backup
4. Verify health checks

### RTO/RPO Targets
- Recovery Time Objective (RTO): 15 minutes
- Recovery Point Objective (RPO): 1 hour (cache data acceptable loss)

---

## Future Enhancements

### Phase 2
- [ ] User-based rate limiting (in addition to IP-based)
- [ ] Response compression (gzip/brotli)
- [ ] Request/response caching at CDN edge
- [ ] Webhook notifications for resolution failures
- [ ] Batch resolution endpoint

### Phase 3
- [ ] GraphQL API alongside REST
- [ ] Real-time WebSocket updates
- [ ] Machine learning for cache prewarming
- [ ] A/B testing framework
- [ ] Multi-region deployment

### Phase 4
- [ ] Plugin architecture for custom resolvers
- [ ] Analytics dashboard
- [ ] Self-service API key management portal
- [ ] Advanced monitoring with distributed tracing
- [ ] Chaos engineering integration

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Redis Best Practices: https://redis.io/docs/manual/
- HTTPX Documentation: https://www.python-httpx.org/
- SlowAPI (Rate Limiting): https://github.com/laurentS/slowapi
- Python Async Best Practices: https://docs.python.org/3/library/asyncio.html
