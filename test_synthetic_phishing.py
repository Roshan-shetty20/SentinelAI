import sys
sys.path.append('backend')
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

urls = [
    "http://secure-update-paypal-account.com/login",
    "https://login.amazon.com.security-check-update.cc/auth",
    "http://192.168.1.100/banking/secure/login.php",
    "https://www.netflix-billing-update.info/secure",
    "https://app-secure-bank.000webhostapp.com/"
]

for u in urls:
    res = client.post("/api/analyze-url", json={"url": u})
    print(f"URL: {u}")
    print(f"Prediction: {res.json().get('prediction').upper()} | Risk: {res.json().get('risk_score')}%")
    print("-" * 50)
