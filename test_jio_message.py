import sys
sys.path.append('backend')
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

message = "Plan expired! Recharge now Jio no. 8822131292 with Rs.349 plan & get Exclusive Offer! JioHotstar + Free AI benefits from Google Gemini & 5000 GB storage + Unlimited 5G data + 2 GB/day, Unlimited Voice, 28 Days. Use PhonePe app & get upto Rs.400 Rewards. T&CA.https://phon.pe/jiol"

response = client.post("/api/analyze-message", json={"message": message})
print(f"Status: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Response text:", response.text)
