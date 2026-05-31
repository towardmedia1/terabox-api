import re
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx

app = FastAPI(
    title="Custom Terabox Downloader API",
    description="Claude Sonnet Powered Production-Ready API Server.",
    version="1.0.0"
)

class TeraboxRequest(BaseModel):
    url: str

# ⚠️ यहाँ आपकी टेराबॉक्स कुकी बिल्कुल सही सेट है
NDUS_COOKIE = "Y-FwX3KteHuidJr6Wm0UxNUyjDD0ceJLYctaZuLr"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}

def format_size(bytes_size: Optional[int]) -> str:
    if not bytes_size:
        return "0 Bytes"
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Terabox Downloader API - Claude Sonnet Powered",
        "endpoints": {
            "GET /fetch": "Query parameter: url (Terabox share link)",
            "POST /api/v1/fetch": "Body: {url: 'terabox_link'}"
        },
        "example": "/fetch?url=https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA"
    }

@app.get("/fetch")
async def fetch_terabox_links_get(url: str = Query(..., description="Terabox share URL")):
    """
    GET endpoint - Query parameter se Terabox URL process karta hai
    Example: /fetch?url=https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA
    """
    input_url = url.strip()
    
    if not input_url:
        raise HTTPException(status_code=400, detail="URL parameter खाली नहीं हो सकता")
    
    if "terabox" not in input_url.lower() and "1024tera" not in input_url.lower():
        raise HTTPException(status_code=400, detail="कृपया केवल वैध Terabox लिंक ही भेजें।")

    async with httpx.AsyncClient(follow_redirects=True, headers=HEADERS, timeout=30.0) as client:
        try:
            # 1. शॉर्ट URL को एक्सपैंड करना
            response = await client.get(input_url)
            final_url = str(response.url)
            
            # 2. सुरल (Share ID) निकालना
            surl_match = re.search(r'surl=([^&]+)', final_url)
            if surl_match:
                surl = surl_match.group(1)
            else:
                # URL से direct extract करना
                surl_match_direct = re.search(r'/s/([^/?]+)', input_url)
                if surl_match_direct:
                    surl = surl_match_direct.group(1)
                else:
                    short_code = final_url.split('/')[-1].split('?')[0]
                    surl = short_code.replace('1', '', 1) if short_code.startswith('1') else short_code

            if not surl or surl == "s":
                raise HTTPException(status_code=400, detail="लिंक से Share ID (surl) नहीं निकाली जा सके।")

            # 3. टेराबॉक्स के असली डेटा शेयर एंडपॉइंट को हिट करना
            api_url = f"https://terabox.com/share/list?shorturl={surl}&root=1&page=1&num=20"
            
            api_headers = HEADERS.copy()
            api_headers["Cookie"] = f"ndus={NDUS_COOKIE}"
            
            api_response = await client.get(api_url, headers=api_headers)
            data = api_response.json()
            
            if data.get("errno") != 0:
                raise HTTPException(status_code=400, detail=f"Terabox API Error: {data.get('errmsg', 'Unknown error')}")
                
            file_list = data.get("list", [])
            if not file_list:
                raise HTTPException(status_code=404, detail="इस साझा लिंक में कोई फाइल नहीं मिली।")
            
            # 4. क्लीन रिस्पॉन्स फॉर्मेट तैयार करना
            formatted_files = []
            for file in file_list:
                size_bytes = int(file.get("size", 0))
                formatted_files.append({
                    "name": file.get("server_filename"),
                    "size_bytes": size_bytes,
                    "size_formatted": format_size(size_bytes),
                    "type": "video" if file.get("category") == "1" else "file",
                    "thumbnail": file.get("thumbs", {}).get("url3") if "thumbs" in file else None,
                    "download_url": file.get("dlink"),  # Direct download link
                    "play_url": file.get("dlink")  # Video play link (same as download)
                })
                
            return {
                "status": "success",
                "author": "Claude Sonnet 4.5 Creator",
                "total_files": len(formatted_files),
                "share_id": surl,
                "data": formatted_files
            }

        except httpx.ConnectTimeout:
            raise HTTPException(status_code=504, detail="कनेक्शन टाइमआउट! टेराबॉक्स सर्वर जवाब नहीं दे रहा है।")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"नेटवर्क एरर: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"इंटरनल सर्वर एरर: {str(e)}")

@app.post("/api/v1/fetch")
async def fetch_terabox_links(payload: TeraboxRequest):
    """
    POST endpoint - Request body se Terabox URL process karta hai
    Body: {"url": "https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA"}
    """
    input_url = payload.url.strip()
    
    if not input_url:
        raise HTTPException(status_code=400, detail="URL खाली नहीं हो सकता")
    
    if "terabox" not in input_url.lower() and "1024tera" not in input_url.lower():
        raise HTTPException(status_code=400, detail="कृपया केवल वैध Terabox लिंक ही भेजें।")

    async with httpx.AsyncClient(follow_redirects=True, headers=HEADERS, timeout=30.0) as client:
        try:
            # 1. शॉर्ट URL को एक्सपैंड करना
            response = await client.get(input_url)
            final_url = str(response.url)
            
            # 2. सुरल (Share ID) निकालना
            surl_match = re.search(r'surl=([^&]+)', final_url)
            if surl_match:
                surl = surl_match.group(1)
            else:
                # URL से direct extract करना
                surl_match_direct = re.search(r'/s/([^/?]+)', input_url)
                if surl_match_direct:
                    surl = surl_match_direct.group(1)
                else:
                    short_code = final_url.split('/')[-1].split('?')[0]
                    surl = short_code.replace('1', '', 1) if short_code.startswith('1') else short_code

            if not surl or surl == "s":
                raise HTTPException(status_code=400, detail="लिंक से Share ID (surl) नहीं निकाली जा सके।")

            # 3. टेराबॉक्स के असली डेटा शेयर एंडपॉइंट को हिट करना
            api_url = f"https://terabox.com/share/list?shorturl={surl}&root=1&page=1&num=20"
            
            api_headers = HEADERS.copy()
            api_headers["Cookie"] = f"ndus={NDUS_COOKIE}"
            
            api_response = await client.get(api_url, headers=api_headers)
            data = api_response.json()
            
            if data.get("errno") != 0:
                raise HTTPException(status_code=400, detail=f"Terabox API Error: {data.get('errmsg', 'Unknown error')}")
                
            file_list = data.get("list", [])
            if not file_list:
                raise HTTPException(status_code=404, detail="इस साझा लिंक में कोई फाइल नहीं मिली।")
            
            # 4. क्लीन रिस्पॉन्स फॉर्मेट तैयार करना
            formatted_files = []
            for file in file_list:
                size_bytes = int(file.get("size", 0))
                formatted_files.append({
                    "name": file.get("server_filename"),
                    "size_bytes": size_bytes,
                    "size_formatted": format_size(size_bytes),
                    "type": "video" if file.get("category") == "1" else "file",
                    "thumbnail": file.get("thumbs", {}).get("url3") if "thumbs" in file else None,
                    "download_url": file.get("dlink"),  # Direct download link
                    "play_url": file.get("dlink")  # Video play link (same as download)
                })
                
            return {
                "status": "success",
                "author": "Claude Sonnet 4.5 Creator",
                "total_files": len(formatted_files),
                "share_id": surl,
                "data": formatted_files
            }

        except httpx.ConnectTimeout:
            raise HTTPException(status_code=504, detail="कनेक्शन टाइमआउट! टेराबॉक्स सर्वर जवाब नहीं दे रहा है।")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"नेटवर्क एरर: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"इंटरनल सर्वर एरर: {str(e)}")