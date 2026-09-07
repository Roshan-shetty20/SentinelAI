import sys
sys.path.append('backend')
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

url = "/api/analyze-url"
headers = {
    "Origin": "http://127.0.0.1:5500",
    "Access-Control-Request-Method": "POST"
}

res = client.options(url, headers=headers)
print("OPTIONS Response:", res.status_code)
print("CORS Headers:", res.headers.get("access-control-allow-origin"))

payload = {"url": "http://secure-update-paypal-account.com/login"}
post_headers = {
    "Origin": "http://127.0.0.1:5500"
}
res = client.post(url, json=payload, headers=post_headers)
print("POST Response:", res.status_code)
print("POST JSON:", res.json())
print("CORS Headers POST:", res.headers.get("access-control-allow-origin"))
