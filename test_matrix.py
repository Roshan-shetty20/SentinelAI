import sys
sys.path.append('backend')
from main import analyze_message, MessageRequest
import asyncio

cases = [
    ("Legitimate recharge, no URL", "Your recharge of Rs.349 was successful. Validity 28 days."),
    ("Legitimate recharge + known safe URL", "Your recharge of Rs.349 was successful. https://hdfcbank.com"),
    ("Legitimate promotion + short URL", "Get 50% off on your next flight! https://phon.pe/xyz"),
    ("Legitimate OTP", "Your OTP is 482931. Do not share it."),
    ("Legitimate bank transaction", "Rs.5000 debited from A/C XX123. https://hdfcbank.com"),
    ("Legitimate ecommerce notification", "Your order has been shipped. Track: https://amzn.to/1234"),
    ("Scam + phishing URL", "Your account is suspended. Update KYC immediately here: https://hdfcbank-kyc-update.com/login"),
    ("Scam + unknown URL", "Your account is suspended. Update KYC immediately here: https://phon.pe/scam-update"),
    ("Credential phishing + URL", "Dear user, your password will expire in 24 hours. Reset now: https://paypal-security-alert.com/verify"),
    ("Exact Jio message", "Plan expired! Recharge now Jio no. 8822131292 with Rs.349 plan & get Exclusive Offer! JioHotstar + Free AI benefits from Google Gemini & 5000 GB storage + Unlimited 5G data + 2 GB/day, Unlimited Voice, 28 Days. Use PhonePe app & get upto Rs.400 Rewards. T&CA.https://phon.pe/jiol")
]

async def test():
    for name, msg in cases:
        req = MessageRequest(message=msg)
        res = analyze_message(req)
        m_risk = res['components']['message_risk']['risk_score'] if 'message_risk' in res['components'] else 0
        u_risk = res['components']['url_risk']['risk_score'] if 'url_risk' in res['components'] else 0
        print(f"{name:35} | Msg: {m_risk:5.2f} | URL: {u_risk:5.2f} | Overall: {res['prediction'].upper():10} ({res['risk_score']:5.2f})")

asyncio.run(test())
