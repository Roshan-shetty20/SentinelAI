import sys
sys.path.append('backend')
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

url = "/api/analyze-url"
payload = {"url": "https://www.reva.edu.in/phd-admissions/?_gl=1%2A136um7i%2A_gcl_au%2AMzY4MzMyNjkyLjE3NzE5MzM0NTc.%22"}

res = client.post(url, json=payload)
print("POST Response:", res.status_code)
print("POST JSON:", res.json())
