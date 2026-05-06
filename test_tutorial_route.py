#!/usr/bin/env python3
"""
Quick test script to verify tutorial video routes are working
"""
import requests
import sys

BASE_URL = "http://localhost:5000"

def test_tutorial_routes():
    print("🧪 Testing Tutorial Video Routes\n")
    print("=" * 60)
    
    # Test valid tutorial videos
    print("\n✅ Testing Valid Tutorial Videos:")
    for i in range(1, 9):
        filename = f"level{i}_tutorial.mp4"
        url = f"{BASE_URL}/tutorial/{filename}"
        
        try:
            response = requests.head(url, timeout=5)
            status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"
            print(f"  Level {i}: {status} - {url}")
        except requests.exceptions.ConnectionError:
            print(f"  ⚠️  Server not running at {BASE_URL}")
            print(f"  Please start the server with: python ITM/backend3ds.py")
            return False
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test invalid requests
    print("\n❌ Testing Invalid Requests (should return 400):")
    invalid_tests = [
        "invalid.mp4",
        "level9_tutorial.mp4",
        "../secret.mp4",
        "level1_tutorial.txt",
    ]
    
    for filename in invalid_tests:
        url = f"{BASE_URL}/tutorial/{filename}"
        try:
            response = requests.head(url, timeout=5)
            status = "✅ Blocked" if response.status_code == 400 else f"⚠️  {response.status_code}"
            print(f"  {filename}: {status}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Route testing complete!")
    print("\nTo test in browser, visit:")
    print(f"  {BASE_URL}/tutorial/level1_tutorial.mp4")
    
    return True

if __name__ == "__main__":
    success = test_tutorial_routes()
    sys.exit(0 if success else 1)
