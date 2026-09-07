import sys
sys.path.append('backend')
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

messages = {
    "OTP": "Your OTP is 482931. Do not share it.",
    "Banking": "Your ATM withdrawal of Rs.2000 was successful.",
    "Telecom": "Your recharge of Rs.349 was successful. Your plan is valid for 28 days.",
    "Promotional": "Exclusive benefits are available with your current plan.",
    "Jio": "Plan expired! Recharge now Jio no. 8822131292 with Rs.349 plan & get Exclusive Offer! JioHotstar + Free AI benefits from Google Gemini & 5000 GB storage + Unlimited 5G data + 2 GB/day, Unlimited Voice, 28 Days. Use PhonePe app & get upto Rs.400 Rewards. T&CA.https://phon.pe/jiol",
    "Adversarial Scam": "Your OTP is 482931. Click this link and enter the OTP to receive your reward."
}

with open('category_test_results.txt', 'w', encoding='utf-8') as f:
    for cat, msg in messages.items():
        f.write("-" * 50 + "\n")
        f.write(f"Category: {cat}\n")
        f.write(f"Message: {msg}\n")
        res = client.post("/api/analyze-message", json={"message": msg})
        if res.status_code == 200:
            data = res.json()
            f.write(f"Message Model (Model 1): {data.get('model_1', {}).get('prediction')} | Confidence: {data.get('model_1', {}).get('confidence')}%\n")
            f.write(f"Overall Prediction: {data.get('prediction')}\n")
        else:
            f.write(f"Error: {res.text}\n")
