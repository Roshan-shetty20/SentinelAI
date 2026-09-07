import sys
sys.path.append('backend')
from main import app
from fastapi.testclient import TestClient
import os

os.environ["SENTINELAI_DEV_MODE"] = "true"

client = TestClient(app)

urls = [
    # Local
    "http://localhost:8888/tree?",
    "http://localhost:8000/",
    "http://127.0.0.1:8000/",
    "http://[::1]:8000/",
    # Trusted
    "https://hdfcbank.com",
    "https://www.hdfcbank.com",
    "https://subdomain.hdfcbank.com",
    "https://icicibank.com",
    # Spoofed (Not Trusted)
    "https://evil-hdfcbank.com",
    "https://hdfcbank.com.evil.com",
    "https://fakeicicibank.com",
    # Legitimate promotional
    "https://www.myntra.com/shoes?utm_source=google",
    "https://www.flipkart.com/offers-list?utm_campaign=diwali",
    # Phishing
    "http://secure-login-verify-account.xyz",
    "http://paypal-security-check-login.xyz"
]

for u in urls:
    res = client.post("/api/analyze-url", json={"url": u})
    data = res.json()
    print(f"URL: {u}")
    print(f"Prediction: {data.get('prediction')} | Reason: {data.get('reasons', [''])[0]}")
    print("-" * 50)
