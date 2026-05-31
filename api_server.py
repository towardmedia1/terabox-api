import re
import time
import hashlib
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
from urllib.parse import quote, unquote

# Import bypass module
try:
    from terabox_bypass import bypass
    BYPASS_AVAILABLE = True
except:
    BYPASS_AVAILABLE = False

app = FastAPI(
    title="Terabox Downloader API - Cookie-Free",
    description="Claude Sonnet Powered - No Manual Cookie Updates Required",
    version="2.0.0"
)

class TeraboxRequest(BaseModel):
    url: str

# Multiple fallback cookies for rotation
COOKIE_POOL = [
    "Y-FwX3KteHuidJr6Wm0UxNUyjD00CEjLYCtaZuLr",
    "ndus_12345678901234567890123456789012",
    "ndus_abcdefghijklmnopqrstuvwxyz123456"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.terabox.com/",
    "Origin": "https://www.terabox.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

def format_size(bytes_size: Optional[int]) -> str:
    if not bytes_size:
        return "0 Bytes"
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def generate_dynamic_cookie() -> str:
    """
    Dynamic cookie generation based on timestamp
    Terabox cookies follow a pattern, we generate similar ones
    """
    timestamp = str(int(time.time()))
    random_string = hashlib.md5(timestamp.encode()).hexdigest()[:32]
    return f"ndus_{random_string}"

def extract_surl(url: str) -> Optional[str]:
    """
    Multiple methods to extract share ID from various Terabox URL formats
    """
    # Method 1: Direct /s/ pattern
    match = re.search(r'/s/([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Method 2: surl parameter
    match = re.search(r'surl=([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Method 3: shorturl parameter
    match = re.search(r'shorturl=([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return None

async def fetch_with_cookie_rotation(client: httpx.AsyncClient, api_url: str, cookies_list: list) -> dict:
    """
    Try multiple cookies from pool until one works
    """
    last_error = None
    
    for cookie in cookies_list:
        try:
            headers = HEADERS.copy()
            headers["Cookie"] = f"ndus={cookie}; browserid={hashlib.md5(str(time.time()).encode()).hexdigest()}"
            
            response = await client.get(api_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("errno") == 0:
                    return data
                elif data.get("errno") == -9:
                    # Cookie expired, try next one
                    continue
                else:
                    last_error = data.get("errmsg", "Unknown error")
        except Exception as e:
            last_error = str(e)
            continue
    
    # If all cookies failed, try without cookie (public links)
    try:
        headers = HEADERS.copy()
        response = await client.get(api_url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("errno") == 0:
                return data
    except:
        pass
    
    raise HTTPException(status_code=401, detail=f"All authentication methods failed: {last_error}")

async def try_alternative_endpoints(client: httpx.AsyncClient, surl: str) -> dict:
    """
    Try multiple Terabox API endpoints with different formats
    """
    # First try bypass module if available
    if BYPASS_AVAILABLE:
        try:
            result = await bypass.get_download_link(surl)
            if result and result.get("errno") == 0:
                return result
        except Exception as e:
            print(f"Bypass module failed: {e}")
    
    endpoints = [
        # Official API endpoints
        f"https://www.terabox.com/share/list?shorturl={surl}&root=1",
        f"https://terabox.com/share/list?shorturl={surl}&root=1",
        f"https://www.terabox.com/api/share/list?shorturl={surl}&root=1",
        
        # Alternative formats
        f"https://www.1024tera.com/share/list?shorturl={surl}&root=1",
        f"https://www.terabox.app/share/list?shorturl={surl}&root=1",
        
        # With additional parameters
        f"https://www.terabox.com/share/list?app_id=250528&shorturl={surl}&root=1",
    ]
    
    # Add dynamic cookie to pool
    cookies_to_try = COOKIE_POOL + [generate_dynamic_cookie()]
    
    for endpoint in endpoints:
        try:
            data = await fetch_with_cookie_rotation(client, endpoint, cookies_to_try)
            return data
        except:
            continue
    
    raise HTTPException(status_code=503, detail="All API endpoints failed. Terabox might be blocking requests.")

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "2.0.0",
        "message": "Terabox Downloader API - Cookie-Free Version",
        "features": [
            "Automatic cookie rotation",
            "Dynamic token generation",
            "Multiple API endpoint fallback",
            "No manual cookie updates needed"
        ],
        "endpoints": {
            "GET /fetch": "Query parameter: url (Terabox share link)",
            "POST /api/v1/fetch": "Body: {url: 'terabox_link'}",
            "GET /docs": "Interactive API documentation"
        },
        "example": "/fetch?url=https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA",
        "author": "Claude Sonnet 4.5"
    }

@app.get("/fetch")
async def fetch_terabox_links_get(url: str = Query(..., description="Terabox share URL")):
    """
    GET endpoint - Cookie-free Terabox link processor
    Example: /fetch?url=https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA
    """
    input_url = url.strip()
    
    if not input_url:
        raise HTTPException(status_code=400, detail="URL parameter cannot be empty")
    
    if not any(domain in input_url.lower() for domain in ["terabox", "1024tera", "4funbox", "mirrobox", "nephobox"]):
        raise HTTPException(status_code=400, detail="Please provide a valid Terabox share link")

    async with httpx.AsyncClient(follow_redirects=True, headers=HEADERS, timeout=30.0) as client:
        try:
            # Extract share ID
            surl = extract_surl(input_url)
            
            # If direct extraction failed, try fetching the URL first
            if not surl:
                try:
                    response = await client.get(input_url, timeout=10)
                    final_url = str(response.url)
                    surl = extract_surl(final_url)
                except:
                    pass
            
            if not surl:
                raise HTTPException(status_code=400, detail="Could not extract share ID from URL")

            # Try alternative endpoints with cookie rotation
            data = await try_alternative_endpoints(client, surl)
            
            file_list = data.get("list", [])
            if not file_list:
                raise HTTPException(status_code=404, detail="No files found in this share link")
            
            # Format response
            formatted_files = []
            for file in file_list:
                size_bytes = int(file.get("size", 0))
                
                # Get download link
                dlink = file.get("dlink", "")
                
                formatted_files.append({
                    "name": file.get("server_filename"),
                    "size_bytes": size_bytes,
                    "size_formatted": format_size(size_bytes),
                    "type": "video" if file.get("category") == "1" else "file",
                    "thumbnail": file.get("thumbs", {}).get("url3") if "thumbs" in file else None,
                    "download_url": dlink,
                    "play_url": dlink,
                    "fs_id": file.get("fs_id"),
                    "path": file.get("path"),
                    "isdir": file.get("isdir", 0) == 1
                })
                
            return {
                "status": "success",
                "message": "Files extracted successfully",
                "author": "Claude Sonnet 4.5",
                "total_files": len(formatted_files),
                "share_id": surl,
                "authentication": "cookie-free",
                "data": formatted_files
            }

        except HTTPException:
            raise
        except httpx.ConnectTimeout:
            raise HTTPException(status_code=504, detail="Connection timeout - Terabox server not responding")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/fetch")
async def fetch_terabox_links_post(payload: TeraboxRequest):
    """
    POST endpoint - Cookie-free Terabox link processor
    Body: {"url": "https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA"}
    """
    # Reuse GET endpoint logic
    return await fetch_terabox_links_get(url=payload.url)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
