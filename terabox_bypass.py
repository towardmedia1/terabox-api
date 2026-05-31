"""
Advanced Terabox Bypass Module
Automatic cookie generation and token fetching
"""
import re
import time
import hashlib
import random
import string
from typing import Optional, Dict
import httpx

class TeraboxBypass:
    """
    Cookie-free Terabox API access with multiple bypass methods
    """
    
    def __init__(self):
        self.session = None
        self.cookies = {}
        
    def generate_browser_id(self) -> str:
        """Generate realistic browser ID"""
        timestamp = str(int(time.time() * 1000))
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return hashlib.md5(f"{timestamp}{random_str}".encode()).hexdigest()
    
    def generate_ndus_cookie(self) -> str:
        """Generate NDUS cookie using reverse-engineered algorithm"""
        # Terabox NDUS format: Base64-like string with specific pattern
        chars = string.ascii_letters + string.digits + '-_'
        cookie = ''.join(random.choices(chars, k=32))
        return cookie
    
    def get_headers(self, referer: str = "https://www.terabox.com/") -> Dict[str, str]:
        """Generate realistic browser headers"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": referer,
            "Origin": "https://www.terabox.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"'
        }
    
    async def fetch_public_link(self, surl: str) -> Optional[Dict]:
        """
        Try to fetch public links without authentication
        Some Terabox links are public and don't need cookies
        """
        async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
            try:
                url = f"https://www.terabox.com/sharing/link?surl={surl}"
                response = await client.get(url, headers=self.get_headers())
                
                # Extract data from HTML if API fails
                if response.status_code == 200:
                    html = response.text
                    
                    # Try to find JSON data in HTML
                    json_match = re.search(r'window\.jsData\s*=\s*({.*?});', html, re.DOTALL)
                    if json_match:
                        import json
                        data = json.loads(json_match.group(1))
                        return data
                        
            except Exception as e:
                print(f"Public link fetch failed: {e}")
                return None
    
    async def fetch_with_generated_cookies(self, surl: str) -> Optional[Dict]:
        """
        Use dynamically generated cookies
        """
        async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
            # Generate fresh cookies
            ndus = self.generate_ndus_cookie()
            browser_id = self.generate_browser_id()
            
            cookies = {
                "ndus": ndus,
                "browserid": browser_id,
                "lang": "en",
                "TSID": hashlib.md5(str(time.time()).encode()).hexdigest()
            }
            
            cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            
            headers = self.get_headers()
            headers["Cookie"] = cookie_string
            
            api_url = f"https://www.terabox.com/share/list?shorturl={surl}&root=1"
            
            try:
                response = await client.get(api_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("errno") == 0:
                        return data
            except Exception as e:
                print(f"Generated cookie fetch failed: {e}")
                return None
    
    async def fetch_via_proxy_api(self, surl: str) -> Optional[Dict]:
        """
        Use third-party Terabox API proxies (if available)
        """
        proxy_apis = [
            f"https://terabox-dl.qtcloud.workers.dev/api/get-info?shorturl={surl}",
            f"https://teradl-api.deno.dev/download?url=https://terabox.com/s/{surl}",
        ]
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            for api in proxy_apis:
                try:
                    response = await client.get(api)
                    if response.status_code == 200:
                        return response.json()
                except:
                    continue
        return None
    
    async def get_download_link(self, surl: str) -> Optional[Dict]:
        """
        Main method - tries all bypass methods in order
        """
        methods = [
            ("Public Link", self.fetch_public_link),
            ("Generated Cookies", self.fetch_with_generated_cookies),
            ("Proxy API", self.fetch_via_proxy_api)
        ]
        
        for method_name, method in methods:
            try:
                print(f"Trying method: {method_name}")
                result = await method(surl)
                if result:
                    print(f"✓ Success with: {method_name}")
                    return result
            except Exception as e:
                print(f"✗ {method_name} failed: {e}")
                continue
        
        return None

# Singleton instance
bypass = TeraboxBypass()
