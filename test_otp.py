import sys
sys.path.append('backend')
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)
res = client.post("/api/analyze-message", json={"message": "Your OTP is 482931. Do not share it."})
print(json.dumps(res.json(), indent=2))
