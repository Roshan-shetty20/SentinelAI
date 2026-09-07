import sys
sys.path.append('backend')
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

url = "/api/analyze-url"
payload = {"url": "https://s.bflcomm.in/BAJAJF/aBN706pG"}

res = client.post(url, json=payload)
print("POST Response:", res.status_code)
print("POST JSON:", res.json())
