"""
Quick test script to verify the API endpoint works
Run: python test_endpoint.py
"""
import requests
import json

API_URL = "http://localhost:8000/api/v1/fetch"
TEST_URL = "https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA"

print("=" * 60)
print("Testing POST /api/v1/fetch endpoint")
print("=" * 60)
print(f"\nAPI URL: {API_URL}")
print(f"Test URL: {TEST_URL}\n")

try:
    response = requests.post(
        API_URL,
        json={"url": TEST_URL},
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS!\n")
        print(json.dumps(data, indent=2))
        
        # Verify required fields
        if "data" in data and len(data["data"]) > 0:
            first_file = data["data"][0]
            print("\n" + "=" * 60)
            print("Verifying required fields:")
            print("=" * 60)
            print(f"✓ name: {first_file.get('name')}")
            print(f"✓ download_url: {first_file.get('download_url')[:50]}...")
            print(f"✓ stream_url: {first_file.get('stream_url')[:50]}...")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error!")
    print("\nMake sure the server is running:")
    print("  python -m uvicorn api_server:app --reload --port 8000")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
