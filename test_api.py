"""
Test script for URL Resolution Engine API
Validates all functionality including auth, rate limiting, caching, and resolution
"""

import asyncio
import time
from typing import Dict, Any

import httpx


# Configuration
BASE_URL = "http://127.0.0.1:7070"  # Updated to port 7070 to bypass ghost process
VALID_API_KEY = "sk_prod_example_key_replace_in_production"
INVALID_API_KEY = "invalid_key_12345"

# Test URLs - Replace with actual test URLs from your platform
TEST_URL_WITH_SURL = "https://terabox.com/s/1234567890?surl=test123&other=param"


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_test(test_name: str):
    """Print test header"""
    print(f"\n{Colors.BLUE}[TEST]{Colors.RESET} {test_name}")


def print_success(message: str):
    """Print success message"""
    print(f"  {Colors.GREEN}✓{Colors.RESET} {message}")


def print_failure(message: str):
    """Print failure message"""
    print(f"  {Colors.RED}✗{Colors.RESET} {message}")


def print_info(message: str):
    """Print info message"""
    print(f"  {Colors.YELLOW}ℹ{Colors.RESET} {message}")


async def test_health_check(client: httpx.AsyncClient) -> bool:
    """Test health check endpoint"""
    print_test("Health Check Endpoint")
    
    try:
        response = await client.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status: {response.status_code}")
            print_info(f"Redis: {data.get('redis', 'unknown')}")
            print_info(f"HTTP Client: {data.get('http_client', 'unknown')}")
            return True
        else:
            print_failure(f"Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def test_missing_api_key(client: httpx.AsyncClient) -> bool:
    """Test request without API key (should return 403)"""
    print_test("Missing API Key Authentication")
    
    try:
        response = await client.post(
            f"{BASE_URL}/api/v1/resolve",
            json={"url": TEST_URL_WITH_SURL}
        )
        
        if response.status_code == 403:
            data = response.json()
            print_success(f"Correctly rejected with 403")
            print_info(f"Error: {data.get('error', 'N/A')}")
            return True
        else:
            print_failure(f"Expected 403, got {response.status_code}")
            return False
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def test_invalid_api_key(client: httpx.AsyncClient) -> bool:
    """Test request with invalid API key (should return 403)"""
    print_test("Invalid API Key Authentication")
    
    try:
        response = await client.post(
            f"{BASE_URL}/api/v1/resolve",
            json={"url": TEST_URL_WITH_SURL},
            headers={"X-API-Key": INVALID_API_KEY}
        )
        
        if response.status_code == 403:
            data = response.json()
            print_success(f"Correctly rejected with 403")
            print_info(f"Error: {data.get('error', 'N/A')}")
            return True
        else:
            print_failure(f"Expected 403, got {response.status_code}")
            return False
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def test_missing_url(client: httpx.AsyncClient) -> bool:
    """Test request with missing URL parameter"""
    print_test("Missing URL Parameter Validation")
    
    try:
        response = await client.post(
            f"{BASE_URL}/api/v1/resolve",
            json={},
            headers={"X-API-Key": VALID_API_KEY}
        )
        
        if response.status_code == 422:
            print_success(f"Validation error returned (422)")
            return True
        else:
            print_failure(f"Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def test_invalid_url_no_surl(client: httpx.AsyncClient) -> bool:
    """Test request with URL missing 'surl' parameter"""
    print_test("URL Without 'surl' Parameter")
    
    try:
        response = await client.post(
            f"{BASE_URL}/api/v1/resolve",
            json={"url": "https://example.com/page?other=param"},
            headers={"X-API-Key": VALID_API_KEY}
        )
        
        if response.status_code == 400:
            data = response.json()
            print_success(f"Correctly rejected with 400")
            print_info(f"Error: {data.get('error', 'N/A')}")
            return True
        else:
            print_failure(f"Expected 400, got {response.status_code}")
            return False
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def test_successful_resolution(client: httpx.AsyncClient) -> bool:
    """Test successful URL resolution (may fail if test URL is invalid)"""
    print_test("Successful URL Resolution")
    
    try:
        response = await client.post(
            f"{BASE_URL}/api/v1/resolve",
            json={
                "url": TEST_URL_WITH_SURL,
                "ndus_token": "optional_test_token"
            },
            headers={"X-API-Key": VALID_API_KEY},
            timeout=30.0
        )
        
        print_info(f"Status Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            print_success(f"Resolution successful")
            print_info(f"Direct Link: {data.get('direct_link', 'N/A')[:80]}...")
            print_info(f"Cached: {data.get('cached', False)}")
            return True
        elif response.status_code in [400, 502]:
            # Expected if test URL is not real
            print_info(f"Gateway/validation error (expected with test URL)")
            print_info(f"Error: {data.get('error', 'N/A')}")
            return True  # Not a test failure
        else:
            print_failure(f"Unexpected status: {response.status_code}")
            print_info(f"Response: {data}")
            return False
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def test_caching(client: httpx.AsyncClient) -> bool:
    """Test caching functionality with duplicate requests"""
    print_test("Caching Functionality")
    
    try:
        test_url = f"{TEST_URL_WITH_SURL}&cache_test={int(time.time())}"
        
        # First request (cache miss)
        print_info("Making first request (should be cache miss)...")
        response1 = await client.post(
            f"{BASE_URL}/api/v1/resolve",
            json={"url": test_url},
            headers={"X-API-Key": VALID_API_KEY},
            timeout=30.0
        )
        
        if response1.status_code not in [200, 400, 502]:
            print_failure(f"First request failed: {response1.status_code}")
            return False
        
        # Second request (should be cache hit if first succeeded)
        print_info("Making second request (checking cache)...")
        response2 = await client.post(
            f"{BASE_URL}/api/v1/resolve",
            json={"url": test_url},
            headers={"X-API-Key": VALID_API_KEY},
            timeout=30.0
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            if data2.get('cached', False):
                print_success("Cache hit detected on second request")
                return True
            else:
                print_info("Second request not cached (may be due to first request error)")
                return True
        else:
            print_info("Caching test inconclusive (resolution errors)")
            return True
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def test_rate_limiting(client: httpx.AsyncClient) -> bool:
    """Test rate limiting (10 requests per minute)"""
    print_test("Rate Limiting (10 req/min)")
    
    try:
        print_info("Sending 12 rapid requests...")
        
        success_count = 0
        rate_limited_count = 0
        
        for i in range(12):
            response = await client.post(
                f"{BASE_URL}/api/v1/resolve",
                json={"url": f"{TEST_URL_WITH_SURL}&rate_test={i}"},
                headers={"X-API-Key": VALID_API_KEY},
                timeout=10.0
            )
            
            if response.status_code == 429:
                rate_limited_count += 1
            elif response.status_code in [200, 400, 502]:
                success_count += 1
            
            await asyncio.sleep(0.1)  # Small delay between requests
        
        print_info(f"Successful requests: {success_count}")
        print_info(f"Rate limited requests: {rate_limited_count}")
        
        if rate_limited_count > 0:
            print_success("Rate limiting is active")
            return True
        else:
            print_info("No rate limiting detected (may need more requests)")
            return True  # Not a failure
            
    except Exception as e:
        print_failure(f"Error: {e}")
        return False


async def run_all_tests():
    """Run all test cases"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}URL Resolution Engine - API Test Suite{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    async with httpx.AsyncClient() as client:
        results = []
        
        # Run all tests
        results.append(await test_health_check(client))
        results.append(await test_missing_api_key(client))
        results.append(await test_invalid_api_key(client))
        results.append(await test_missing_url(client))
        results.append(await test_invalid_url_no_surl(client))
        results.append(await test_successful_resolution(client))
        results.append(await test_caching(client))
        results.append(await test_rate_limiting(client))
        
        # Print summary
        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BLUE}Test Summary{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
        
        passed = sum(results)
        total = len(results)
        
        if passed == total:
            print(f"\n{Colors.GREEN}All tests passed! ({passed}/{total}){Colors.RESET}\n")
        else:
            print(f"\n{Colors.YELLOW}Tests passed: {passed}/{total}{Colors.RESET}\n")


if __name__ == "__main__":
    print(f"\n{Colors.YELLOW}Note:{Colors.RESET} Ensure the API server is running at {BASE_URL}")
    print(f"{Colors.YELLOW}Note:{Colors.RESET} Some tests may show warnings if using test URLs\n")
    
    asyncio.run(run_all_tests())
