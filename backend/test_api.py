import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000/api"
    
    try:
        # Test products endpoint
        response = requests.get(f"{base_url}/products/", timeout=5)
        print(f"Products API: Status {response.status_code}")
        
        # Test stock levels endpoint
        response = requests.get(f"{base_url}/inventory/stock-levels/", timeout=5)
        print(f"Stock Levels API: Status {response.status_code}")
        
        if response.status_code == 401:
            print("✓ API endpoints are working but require authentication (expected)")
        elif response.status_code == 200:
            data = response.json()
            print(f"✓ Success! Found {len(data)} items")
        else:
            print(f"Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
