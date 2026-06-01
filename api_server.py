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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.terabox.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
        try:
            # Try multiple URL formats to expand the short link
            urls_to_try = [
                f"https://terabox.com/s/{surl}",
                f"https://www.terabox.com/s/{surl}",
                f"https://1024tera.com/s/{surl}",
                f"https://www.1024tera.com/s/{surl}",
            ]
            
            final_url = None
            expanded_surl = surl
            
            # Try to expand the URL and extract surl
            for url in urls_to_try:
                try:
                    response = await client.get(url, headers=headers, timeout=15)
                    final_url = str(response.url)
                    
                    # Extract surl from various URL patterns
                    patterns = [
                        r'surl=([A-Za-z0-9_-]+)',
                        r'/sharing/link\?surl=([A-Za-z0-9_-]+)',
                        r'/share/link\?surl=([A-Za-z0-9_-]+)',
                        r'/s/1([A-Za-z0-9_-]+)',  # Handle 1024tera format
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, final_url)
                        if match:
                            expanded_surl = match.group(1)
                            break
                    
                    # If we got a valid response, break
                    if response.status_code == 200:
                        break
                        
                except Exception as e:
                    continue
            
            # Now call the API with the extracted surl
            api_endpoints = [
                f"https://www.terabox.com/share/list?shorturl={expanded_surl}&root=1",
                f"https://terabox.com/share/list?shorturl={expanded_surl}&root=1",
                f"https://www.terabox.com/api/share/list?shorturl={expanded_surl}&root=1",
            ]
            
            api_data = None
            last_error = None
            
            for api_url in api_endpoints:
                try:
                    api_response = await client.get(api_url, headers=headers, timeout=15)
                    
                    if api_response.status_code == 200:
                        data = api_response.json()
                        
                        # Check if we got valid data
                        if data.get("errno") == 0:
                            api_data = data
                            break
                        else:
                            last_error = data.get('errmsg', 'Unknown error')
                            
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if not api_data:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Failed to fetch TeraBox data: {last_error or 'All endpoints failed'}"
                )
            
            return api_data
            
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
    
    # Extract required parameters from response - try multiple locations
    uk = data.get("uk") or data.get("share_uk") or data.get("user_id")
    shareid = data.get("shareid") or data.get("share_id") or data.get("shareId")
    
    # If still not found, try to extract from the first file
    if not uk and file_list:
        uk = file_list[0].get("uk") or file_list[0].get("owner_id")
    
    if not shareid and file_list:
        shareid = file_list[0].get("shareid") or file_list[0].get("share_id")
    
    # Last resort: try to get from URL or use surl
    if not shareid:
        shareid = data.get("share_link_id") or surl
    
    if not uk or not shareid:
        # Return files without stream URLs if we can't generate them
        results = []
        for file in file_list:
            filename = file.get("server_filename")
            size = file.get("size", 0)
            category = file.get("category")
            download_url = file.get("dlink", "")
            
            results.append({
                "name": filename,
                "filename": filename,
                "size": size,
                "size_formatted": format_size(size),
                "type": "video" if category == "1" else "file",
                "stream_url": download_url,  # Use dlink as fallback
                "download_url": download_url,
                "fs_id": file.get("fs_id"),
                "thumbnail": file.get("thumbs", {}).get("url3") if "thumbs" in file else None
            })
        
        return {
            "status": "success",
            "total_files": len(results),
            "data": results,
            "files": results,
            "warning": "Could not generate stream URLs, using direct links"
        }
    
    # Process files with proper stream URLs
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
    
    return {
        "status": "success",
        "total_files": len(results),
        "data": results,
        "files": results
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
