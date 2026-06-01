# 🎬 TeraBox Video Player & Downloader

A seamless, cookie-less TeraBox video streaming and download system built with FastAPI and modern frontend technologies.

## ✨ Features

- ✅ **Cookie-less Technology** - No manual cookie management required
- ✅ **Direct Streaming** - Extract and play videos instantly
- ✅ **One-Click Download** - Download files directly to your device
- ✅ **Premium Dark UI** - Beautiful, responsive interface
- ✅ **Real-time Extraction** - Fetches fs_id, uk, and shareid dynamically
- ✅ **CORS Enabled** - Works from any domain

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn api_server:app --reload --port 8000

# Open browser
http://localhost:8000
```

### Deploy to Render/Heroku

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn api_server:app --host 0.0.0.0 --port $PORT
```

## 📡 API Endpoints

### GET /
Serves the frontend interface

### GET /api/extract?url={terabox_url}
Extract video streaming and download links

**Parameters:**
- `url` - TeraBox share URL

**Response:**
```json
{
  "status": "success",
  "total_files": 1,
  "files": [
    {
      "filename": "video.mp4",
      "size": 123456789,
      "size_formatted": "117.74 MB",
      "type": "video",
      "stream_url": "https://terabox.com/share/streaming?...",
      "download_url": "https://terabox.com/...",
      "fs_id": "123456",
      "thumbnail": "https://..."
    }
  ]
}
```

### POST /api/extract
Same as GET but accepts JSON body:
```json
{
  "url": "https://terabox.com/s/1xxxxx"
}
```

### GET /health
Health check endpoint

## 🎯 How It Works

1. **Extract Share ID** - Parses TeraBox URL to get surl
2. **Fetch Public Data** - Calls TeraBox public API without cookies
3. **Extract Parameters** - Gets fs_id, uk, and shareid from response
4. **Generate Stream URL** - Creates direct playback link
5. **Serve to Frontend** - Returns streaming and download URLs

## 🔧 Technology Stack

- **Backend:** FastAPI (Python)
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **HTTP Client:** httpx (async)
- **Icons:** Font Awesome 6

## 🌐 Supported URLs

- `https://terabox.com/s/xxxxx`
- `https://1024tera.com/s/xxxxx`
- `https://terabox.com/sharing/link?surl=xxxxx`

## 📝 License

MIT License - Free to use and modify

## ⚠️ Disclaimer

This tool is for educational purposes. Please respect TeraBox's terms of service and copyright laws.
