import re
import httpx
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

app = FastAPI(
    title="TeraBox Video Player & Downloader",
    description="Cookie-less TeraBox streaming and download system",
    version="3.0.0"
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
        r'/s/([A-Za-z0-9_-]+)',
        r'surl=([A-Za-z0-9_-]+)',
        r'shorturl=([A-Za-z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

async def get_terabox_data(surl: str) -> dict:
    """Fetch TeraBox data from public endpoint without cookies"""
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        # Expand short link first
        short_url = f"https://terabox.com/s/{surl}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.terabox.com/",
        }
        
        try:
            # Get the expanded URL
            response = await client.get(short_url, headers=headers)
            final_url = str(response.url)
            
            # Extract surl from final URL if needed
            surl_match = re.search(r'surl=([^&]+)', final_url)
            if surl_match:
                surl = surl_match.group(1)
            
            # Call public API endpoint
            api_url = f"https://terabox.com/share/list?shorturl={surl}&root=1"
            api_response = await client.get(api_url, headers=headers)
            
            if api_response.status_code != 200:
                raise HTTPException(status_code=api_response.status_code, detail="Failed to fetch TeraBox data")
            
            data = api_response.json()
            
            if data.get("errno") != 0:
                raise HTTPException(status_code=400, detail=f"TeraBox API Error: {data.get('errmsg', 'Unknown error')}")
            
            return data
            
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

def generate_stream_url(fs_id: str, uk: str, shareid: str) -> str:
    """Generate direct bypass playback stream URL"""
    return f"https://terabox.com/share/streaming?shareid={shareid}&uk={uk}&fs_id={fs_id}"

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend HTML at root"""
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Frontend not found</h1>")

@app.get("/api/extract")
async def extract_video_get(url: str = Query(..., description="TeraBox share URL")):
    """GET endpoint - Extract video streaming and download links from TeraBox URL"""
    return await extract_video(url)

@app.post("/api/v1/fetch")
async def extract_video_post(request: TeraBoxRequest):
    """POST endpoint - Extract video streaming and download links from TeraBox URL"""
    return await extract_video(request.url)

async def extract_video(url: str):
    """Extract video streaming and download links from TeraBox URL"""
    
    # Extract surl
    surl = extract_surl(url)
    if not surl:
        raise HTTPException(status_code=400, detail="Invalid TeraBox URL. Could not extract share ID.")
    
    # Get TeraBox data
    data = await get_terabox_data(surl)
    
    # Extract file list
    file_list = data.get("list", [])
    if not file_list:
        raise HTTPException(status_code=404, detail="No files found in this share link")
    
    # Extract required parameters from response
    uk = data.get("uk")
    shareid = data.get("shareid")
    
    if not uk or not shareid:
        raise HTTPException(status_code=500, detail="Failed to extract required parameters (uk, shareid)")
    
    # Process files
    results = []
    for file in file_list:
        fs_id = file.get("fs_id")
        filename = file.get("server_filename")
        size = file.get("size", 0)
        category = file.get("category")
        
        if not fs_id:
            continue
        
        # Generate stream URL
        stream_url = generate_stream_url(str(fs_id), str(uk), str(shareid))
        
        # Get direct download link if available
        download_url = file.get("dlink", stream_url)
        
        results.append({
            "name": filename,  # Changed from "filename" to "name" for frontend compatibility
            "filename": filename,
            "size": size,
            "size_formatted": format_size(size),
            "type": "video" if category == "1" else "file",
            "stream_url": stream_url,
            "download_url": download_url,
            "fs_id": fs_id,
            "thumbnail": file.get("thumbs", {}).get("url3") if "thumbs" in file else None
        })
    
    return {
        "status": "success",
        "total_files": len(results),
        "data": results,  # Changed from "files" to "data" for frontend compatibility
        "files": results  # Keep both for backward compatibility
    }

def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size"""
    if not bytes_size:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "3.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
