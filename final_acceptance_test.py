import sys
import traceback
sys.path.append('backend')
from main import analyze_message, MessageRequest
from fastapi import HTTPException
from unittest.mock import patch
import language_utils
language_utils._translation_cache.clear()

tests = [
    ("1. English legitimate message", "Meeting is scheduled for 10 AM tomorrow in the main conference room. Let me know if you can make it."),
    ("2. English phishing message", "URGENT: Your account has been compromised. Please update your payment details immediately to prevent suspension."),
    ("3. Hindi phishing message", "आपका बैंक खाता ब्लॉक कर दिया गया है। अपना केवाईसी अपडेट करें।"),
    ("4. Tamil/Malayalam Unicode message", "നിങ്ങളുടെ അക്കൗണ്ട് മരവിപ്പിച്ചു. ഉടൻ അപ്ഡേറ്റ് ചെയ്യുക"),
    ("5. Mixed-language phishing", "Tumhara bank account suspend ho gaya hai, please update your KYC immediately."),
    ("6. Plain malicious URL", "http://secure-update-paypal-account.com/login"),
    ("7. Markdown malicious URL", "[Click here to verify](http://secure-update-paypal-account.com/login)"),
    ("8. Safe URL", "https://www.google.com"),
    ("9. Malicious message + safe URL", "URGENT: Your account has been compromised. Check https://www.google.com"),
    ("10. Safe message + malicious URL", "Here is the document you requested: http://secure-update-paypal-account.com/login"),
]

print("=== SENTINELAI FINAL ACCEPTANCE TESTS ===\n")

for name, text in tests:
    try:
        req = MessageRequest(message=text)
        res = analyze_message(req)
        
        pred = res['prediction']
        risk = res['risk_score']
        mode = res.get('explainable_ai', {}).get('language_info', {}).get('language_mode', 'N/A')
        urls = res.get('url_results', [])
        url_count = len(urls)
        
        print(f"[{name}]")
        print(f"Prediction: {pred.upper()} | Risk: {risk} | Mode: {mode} | URLs Extracted: {url_count}")
        if urls:
            print(f"URL: {urls[0]['url']} -> {urls[0]['prediction'].upper()} (Risk: {urls[0]['risk_score']})")
        print("-" * 50)
    except Exception as e:
        print(f"[{name}] FAILED: {str(e)}")
        print("-" * 50)

# 11. Translation failure + malicious URL
print("[11. Translation failure + malicious URL]")
try:
    with patch('language_utils.get_translator') as mock_trans:
        mock_trans.side_effect = Exception('API Timeout Simulated')
        req = MessageRequest(message="आपका बैंक खाता ब्लॉक: http://secure-update-paypal-account.com/login")
        res = analyze_message(req)
        pred = res['prediction']
        risk = res['risk_score']
        rev = res.get('explainable_ai', {}).get('language_info', {}).get('requires_manual_review')
        urls = res.get('url_results', [])
        
        print(f"Prediction: {pred.upper()} | Risk: {risk} | Manual Review: {rev}")
        if urls:
            print(f"URL: {urls[0]['url']} -> {urls[0]['prediction'].upper()} (Risk: {urls[0]['risk_score']})")
        print("-" * 50)
except Exception as e:
    print(f"FAILED: {str(e)}")
    print("-" * 50)

# 12. Empty/malformed request
print("[12. Empty/malformed request]")
try:
    req = MessageRequest(message="   ")
    res = analyze_message(req)
    print("FAILED: Should have thrown 400 Bad Request")
except HTTPException as he:
    print(f"SUCCESS: Caught expected HTTP {he.status_code}: {he.detail}")
except Exception as e:
    print(f"FAILED: Wrong exception: {str(e)}")
print("-" * 50)

