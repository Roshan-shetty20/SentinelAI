import sys
sys.path.append('backend')
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

messages = [
    "Your account has been suspended. Verify now.",
    "आपका अकाउंट बंद कर दिया गया है। अभी सत्यापित करें।",
    "Aapka account suspend ho gaya hai, abhi verify karo.",
    "आपका account verify नहीं हुआ। Click here.",
    "ನಿಮ್ಮ ಖಾತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
    "உங்கள் கணக்கை சரிபார்க்கவும்.",
    "Your OTP is 482931. Do not share it.",
    "Congratulations! You won Rs.5000.",
    "Your account requires verification: https://example.com/verify",
    "",
    "   ",
    "Plan expired! Recharge now Jio no. 8822131292 with Rs.349 plan & get Exclusive Offer! JioHotstar + Free AI benefits from Google Gemini & 5000 GB storage + Unlimited 5G data + 2 GB/day, Unlimited Voice, 28 Days. Use PhonePe app & get upto Rs.400 Rewards. T&CA.https://phon.pe/jiol"
]

with open('multilingual_test_results.txt', 'w', encoding='utf-8') as f:
    for msg in messages:
        f.write("-" * 50 + "\n")
        f.write(f"Testing message: {msg}\n")
        res = client.post("/api/analyze-message", json={"message": msg})
        f.write(f"Status: {res.status_code}\n")
        if res.status_code == 200:
            data = res.json()
            f.write(f"Prediction: {data.get('prediction')} | Confidence: {data.get('confidence')}\n")
            f.write(f"Language: {data.get('detected_language')} | Translation Success: {data.get('translation_success')}\n")
            if data.get('translation_success'):
                f.write(f"Translated Text: {data.get('translated_message')}\n")
            if 'url_results' in data and data['url_results']:
                f.write(f"URL Analysis: {json.dumps(data['url_results'], indent=2)}\n")
        else:
            f.write(f"Error: {res.text}\n")
