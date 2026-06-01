import re
import httpx
import json
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os

app = FastAPI(
    title="TeraBox Video Player & Downloader",
    description="Cookie-less TeraBox streaming and download system",
    version="4.0.0"
)

# Configure CORS - Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TeraBoxRequest(BaseModel):
    url: str

def extract_surl(url: str) -> Optional[str]:
    """Extract share ID from TeraBox URL"""
    patterns = [
        r'/s/1?([A-Za-z0-9_-]+)',
        r'surl=([A-Za-z0-9_-]+)',
        r'shorturl=([A-Za-z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

async def fetch_with_fallback(client: httpx.AsyncClient, urls: list, headers: dict) -> Optional[Dict[str, Any]]:
    """Try multiple endpoints with fallback logic"""
    last_error = None
    
    for url in urls:
        try:
            response = await client.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Check if response is JSON
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type:
                    data = response.json()
                    
                    # Check if we got valid data
                    if isinstance(data, dict) and data.get("errno") == 0:
                        return data
                    else:
                        last_error = data.get('errmsg', 'Invalid response from API')
                else:
                    # HTML response, try next endpoint
                    last_error = "Received HTML instead of JSON"
                    continue
                    
        except json.JSONDecodeError:
            last_error = "Invalid JSON response"
            continue
        except httpx.TimeoutException:
            last_error = "Request timeout"
            continue
        except Exception as e:
            last_error = str(e)
            continue
    
    return None

async def get_terabox_data(surl: str) -> dict:
    """Fetch TeraBox data from public endpoint without cookies - with robust fallback"""
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.terabox.com/",
            "Origin": "https://www.terabox.com",
            "Connection": "keep-alive",
        }
        
        try:
            # Step 1: Try to expand the URL
            expansion_urls = [
                f"https://www.terabox.com/s/1{surl}",
                f"https://terabox.com/s/1{surl}",
                f"https://www.1024tera.com/s/1{surl}",
                f"https://1024tera.com/s/1{surl}",
            ]
            
            expanded_surl = surl
            
            for url in expansion_urls:
                try:
                    response = await client.get(url, headers=headers, timeout=10)
                    final_url = str(response.url)
                    
                    # Extract surl from redirected URL
                    patterns = [
                        r'surl=([A-Za-z0-9_-]+)',
                        r'/sharing/link\?surl=([A-Za-z0-9_-]+)',
                        r'/share/link\?surl=([A-Za-z0-9_-]+)',
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, final_url)
                        if match:
                            expanded_surl = match.group(1)
                            break
                    
                    if response.status_code == 200:
                        break
                        
                except Exception:
                    continue
            
            # Step 2: Try multiple API endpoints with fallback
            api_endpoints = [
                f"https://www.terabox.com/share/list?shorturl={expanded_surl}&root=1",
                f"https://terabox.com/share/list?shorturl={expanded_surl}&root=1",
                f"https://www.terabox.com/api/shorturlinfo?shorturl={expanded_surl}",
                f"https://terabox.com/api/shorturlinfo?shorturl={expanded_surl}",
                f"https://www.1024tera.com/share/list?shorturl={expanded_surl}&root=1",
            ]
            
            api_data = await fetch_with_fallback(client, api_endpoints, headers)
            
            if not api_data:
                # Final fallback: return minimal structure
                return {
                    "errno": 0,
                    "list": [],
                    "uk": None,
                    "shareid": expanded_surl,
                    "fallback": True,
                    "message": "Using fallback mode - limited data available"
                }
            
            return api_data
            
        except Exception as e:
            # Return fallback structure instead of raising exception
            return {
                "errno": 0,
                "list": [],
                "uk": None,
                "shareid": surl,
                "fallback": True,
                "error": str(e),
                "message": "Fallback mode activated"
            }

def generate_stream_url(fs_id: str, uk: str, shareid: str) -> str:
    """Generate direct bypass playback stream URL"""
    return f"https://terabox.com/share/streaming?shareid={shareid}&uk={uk}&fs_id={fs_id}"

def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size"""
    if not bytes_size:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend HTML at root"""
    try:
        if os.path.exists("index.html"):
            with open("index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read(), status_code=200)
        else:
            return HTMLResponse(
                content="<h1>Frontend not found</h1><p>index.html is missing</p>",
                status_code=404
            )
    except Exception as e:
        return HTMLResponse(
            content=f"<h1>Error loading frontend</h1><p>{str(e)}</p>",
            status_code=500
        )

@app.get("/api/extract")
async def extract_video_get(url: str = Query(..., description="TeraBox share URL")):
    """GET endpoint - Extract video streaming and download links from TeraBox URL"""
    try:
        return await extract_video(url)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": str(e),
                "message": "Internal server error occurred"
            }
        )

@app.post("/api/v1/fetch")
async def extract_video_post(request: TeraBoxRequest):
    """POST endpoint - Extract video streaming and download links from TeraBox URL"""
    try:
        # Wrap entire logic in try-except to prevent 500 errors
        result = await extract_video(request.url)
        return JSONResponse(content=result, status_code=200)
    except HTTPException as he:
        # Handle known HTTP exceptions
        return JSONResponse(
            status_code=he.status_code,
            content={
                "status": "error",
                "detail": he.detail,
                "message": "Request failed"
            }
        )
    except Exception as e:
        # Catch all other exceptions and return structured error
        return JSONResponse(
            status_code=200,  # Return 200 to prevent frontend errors
            content={
                "status": "error",
                "detail": str(e),
                "message": "Failed to process request. Please check the URL and try again.",
                "total_files": 0,
                "data": [],
                "files": []
            }
        )

async def extract_video(url: str) -> dict:
    """Extract video streaming and download links from TeraBox URL"""
    
    try:
        # Extract surl
        surl = extract_surl(url)
        if not surl:
            return {
                "status": "error",
                "detail": "Invalid TeraBox URL. Could not extract share ID.",
                "total_files": 0,
                "data": [],
                "files": []
            }
        
        # Get TeraBox data with fallback
        data = await get_terabox_data(surl)
        
        # Extract file list
        file_list = data.get("list", [])
        
        if not file_list:
            return {
                "status": "error",
                "detail": "No files found in this share link. The link may be invalid or expired.",
                "total_files": 0,
                "data": [],
                "files": [],
                "fallback": data.get("fallback", False)
            }
        
        # Extract required parameters from response
        uk = data.get("uk") or data.get("share_uk") or data.get("user_id")
        shareid = data.get("shareid") or data.get("share_id") or data.get("shareId")
        
        # Try to extract from first file if not found
        if not uk and file_list:
            uk = file_list[0].get("uk") or file_list[0].get("owner_id")
        
        if not shareid and file_list:
            shareid = file_list[0].get("shareid") or file_list[0].get("share_id")
        
        # Last resort: use surl
        if not shareid:
            shareid = data.get("share_link_id") or surl
        
        # Process files
        results = []
        for file in file_list:
            try:
                fs_id = file.get("fs_id")
                filename = file.get("server_filename", "Unknown")
                size = file.get("size", 0)
                category = file.get("category")
                
                if not fs_id:
                    continue
                
                # Generate URLs
                if uk and shareid:
                    stream_url = generate_stream_url(str(fs_id), str(uk), str(shareid))
                else:
                    stream_url = file.get("dlink", "")
                
                download_url = file.get("dlink", stream_url)
                
                results.append({
                    "name": filename,
                    "filename": filename,
                    "size": size,
                    "size_formatted": format_size(size),
                    "type": "video" if category == "1" else "file",
                    "stream_url": stream_url,
                    "download_url": download_url,
                    "fs_id": fs_id,
                    "thumbnail": file.get("thumbs", {}).get("url3") if "thumbs" in file else None
                })
            except Exception:
                # Skip problematic files
                continue
        
        if not results:
            return {
                "status": "error",
                "detail": "Could not process any files from the share link",
                "total_files": 0,
                "data": [],
                "files": []
            }
        
        return {
            "status": "success",
            "total_files": len(results),
            "data": results,
            "files": results,
            "warning": "Using fallback mode" if data.get("fallback") else None
        }
        
    except Exception as e:
        # Final catch-all
        return {
            "status": "error",
            "detail": f"Unexpected error: {str(e)}",
            "message": "Please try again or check if the URL is valid",
            "total_files": 0,
            "data": [],
            "files": []
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "4.0.0", "service": "TeraBox API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
