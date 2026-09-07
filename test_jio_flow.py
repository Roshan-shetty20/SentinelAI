import sys
sys.path.append('backend')
from main import analyze_message, MessageRequest
import asyncio

async def test():
    req = MessageRequest(message="Plan expired! Recharge now Jio no. 8822131292 with Rs.349 plan & get Exclusive Offer! JioHotstar + Free AI benefits from Google Gemini & 5000 GB storage + Unlimited 5G data + 2 GB/day, Unlimited Voice, 28 Days. Use PhonePe app & get upto Rs.400 Rewards. T&CA.https://phon.pe/jiol")
    res = analyze_message(req)
    print("Message Risk:", res['components']['message_risk']['risk_score'])
    print("URL Risk:", res['components']['url_risk']['risk_score'])
    print("Overall Prediction:", res['prediction'])
    print("Overall Risk:", res['risk_score'])
    print("URL Results:", res['url_results'])

asyncio.run(test())
