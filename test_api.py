"""
Quick API test script
Usage: python test_api.py
"""
import requests
import json

# Change this to your deployed API URL
API_URL = "http://localhost:8000/api/v1/fetch"

# Test Terabox URL
TEST_URL = "https://1024tera.com/s/1OePBz6N_MWXzxw86nbpErA"

def test_api():
    print("🧪 Testing Terabox API...")
    print(f"📡 API URL: {API_URL}")
    print(f"🔗 Test URL: {TEST_URL}\n")
    
    try:
        response = requests.post(
            API_URL,
            json={"url": TEST_URL},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!\n")
            print(f"📁 Total Files: {data.get('total_files')}")
            print(f"🆔 Share ID: {data.get('share_id')}")
            print(f"🔐 Auth Method: {data.get('authentication')}\n")
            
            print("📄 Files:")
            print("-" * 60)
            for idx, file in enumerate(data.get('data', []), 1):
                print(f"\n{idx}. {file.get('name')}")
                print(f"   Size: {file.get('size_formatted')}")
                print(f"   Type: {file.get('type')}")
                print(f"   Download: {file.get('download_url')[:50]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("Make sure the API server is running:")
        print("   python -m uvicorn api_server:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_api()
