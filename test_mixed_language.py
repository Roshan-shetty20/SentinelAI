import sys
import io
import json
sys.path.append('backend')
from main import analyze_message, MessageRequest, message_model
from unittest.mock import patch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

message_model.multi_class = 'ovr'

cases = [
    ("English-only", "Your account will be suspended. Verify immediately."),
    ("Hindi-only", "आपका बैंक खाता बंद कर दिया जाएगा। तुरंत सत्यापन करें।"),
    ("Hinglish + English threat", "Tumhara account suspend ho gaya hai, verify now."),
    ("Hinglish regional threat", "Tumhara bank khata band ho gaya hai, abhi update karo."),
    ("Hinglish code-switching", "Aaj payment karna hai, warna account band ho jayega."),
    ("Legitimate mixed", "Kal meeting attend karna mat bhulna at 10 AM."),
    ("Legitimate Kannada", "Nale office ge barthiya? Let me know."),
    ("URL + Mixed", "Tumhara bank khata block ho gaya hai, update karo: https://example.com/login"),
    ("Markdown + Mixed", "Tumhara bank khata block ho gaya hai. [Update account](https://example.com/login)"),
    ("Adversarial minimal English", "Nimma bank khate block agide, details kodi https://example.com")
]

print("=== TESTING MIXED LANGUAGE ROUTING ===")
for name, text in cases:
    res = analyze_message(MessageRequest(message=text))
    mode = res.get("explainable_ai", {}).get("language_info", {}).get("language_mode", "unknown")
    status = res.get("explainable_ai", {}).get("language_info", {}).get("translation_status", "unknown")
    print(f"\nTest: {name}")
    print(f"Message: {text}")
    print(f"Mode: {mode} | Translation: {status}")
    print(f"Risk: {res['risk_score']} | Class: {res['prediction']}")

print("\n=== TESTING TRANSLATION FAILURE ON MIXED ===")
with patch('backend.language_utils.get_translator') as mock_trans:
    mock_trans.side_effect = Exception('API Timeout')
    # Use un-cached text so mock triggers
    res = analyze_message(MessageRequest(message="NEW Tumhara bank khata block ho gaya hai."))
    xai = res.get("explainable_ai", {}).get("language_info", {})
    print(f"Mode: {xai.get('language_mode')} | Translation: {xai.get('translation_status')}")
    print(f"Rev_Req: {xai.get('requires_manual_review')} | Class: {res['prediction']}")
