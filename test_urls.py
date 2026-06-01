"""
Test script for various TeraBox URL formats
Run: python test_urls.py
"""
import asyncio
import httpx
from api_server import extract_surl, get_terabox_data

# Test URLs
test_urls = [
    "https://terabox.com/s/1OePBz6N_MWXzxw86nbpErA",
    "https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA",
    "https://www.terabox.com/s/1OePBz6N_MWXzxw86nbpErA",
    "https://terabox.com/sharing/link?surl=OePBz6N_MWXzxw86nbpErA",
]

async def test_url(url):
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    print(f"{'='*60}")
    
    try:
        # Extract surl
        surl = extract_surl(url)
        print(f"✓ Extracted surl: {surl}")
        
        # Get data
        data = await get_terabox_data(surl)
        
        # Check for required fields
        uk = data.get("uk")
        shareid = data.get("shareid")
        file_list = data.get("list", [])
        
        print(f"✓ UK: {uk}")
        print(f"✓ ShareID: {shareid}")
        print(f"✓ Files found: {len(file_list)}")
        
        if file_list:
            first_file = file_list[0]
            print(f"✓ First file: {first_file.get('server_filename')}")
            print(f"✓ Size: {first_file.get('size')} bytes")
            print(f"✓ FS_ID: {first_file.get('fs_id')}")
        
        print(f"\n✅ SUCCESS!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

async def main():
    print("="*60)
    print("TeraBox URL Format Testing")
    print("="*60)
    
    for url in test_urls:
        await test_url(url)
    
    print(f"\n{'='*60}")
    print("Testing Complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
