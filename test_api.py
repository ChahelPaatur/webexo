import requests
import json

# Test data - sample CSV content
test_csv = """feature1,feature2,feature3,feature4,feature5
0.5,0.3,0.8,0.6,0.4
0.2,0.7,0.5,0.3,0.9
0.8,0.4,0.6,0.7,0.2"""

# Test the local API
url = "http://127.0.0.1:5001/api/predict"

try:
    print("🧪 Testing ExoML API...")
    print(f"📡 Sending request to {url}")
    
    response = requests.post(
        url,
        json={"data": test_csv},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS! API is working\n")
        print(json.dumps(result, indent=2))
        print(f"\n🪐 Exoplanet Detected: {result.get('isExoplanet')}")
        print(f"📊 Confidence: {result.get('confidence')}%")
        print(f"🌍 Planet Type: {result.get('planetType')}")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Error connecting to server: {str(e)}")
    print("\n💡 Make sure the Flask server is running:")
    print("   python app.py")

