import json
import sys
import time
sys.path.append('backend')
from main import analyze_message, MessageRequest, message_model

message_model.multi_class = 'ovr'

audit_dataset = [
    # --- 3. ZERO-ENGLISH-THREAT TESTS ---
    {
        "id": "zero_eng_1",
        "lang": "hi",
        "category": "malicious",
        "text": "आपका बैंक खाता बंद हो गया है। कृपया अपडेट करें: http://evil.com/login",
        "desc": "Hindi pure threat with URL"
    },
    {
        "id": "zero_eng_2",
        "lang": "ml",
        "category": "malicious",
        "text": "നിങ്ങളുടെ അക്കൗണ്ട് മരവിപ്പിച്ചു. ക്ലിക്ക് ചെയ്യുക: http://fraud.com",
        "desc": "Malayalam pure threat with URL"
    },
    {
        "id": "zero_eng_3",
        "lang": "ta",
        "category": "malicious",
        "text": "உங்கள் கணக்கு முடக்கப்பட்டுள்ளது. http://bad.com",
        "desc": "Tamil pure threat with URL"
    },
    # --- 4. MIXED-LANGUAGE EVASION TESTS ---
    {
        "id": "evasion_1",
        "lang": "mixed",
        "category": "malicious",
        "text": "Tumhara bank khata b.l.o.c.k ho gaya hai update karo.",
        "desc": "Punctuation between threat words"
    },
    {
        "id": "evasion_2",
        "lang": "mixed",
        "category": "malicious",
        "text": "Tumhara account suspend ho gaya hai. Account account account suspend suspend verify verify. Please update.",
        "desc": "Repeated English filler words"
    },
    {
        "id": "evasion_3",
        "lang": "mixed",
        "category": "malicious",
        "text": "Tumhara b4nk 4ccount susp3nd ho gaya hai. Verify now.",
        "desc": "Numbers inserted between words"
    },
    # --- 5. FALSE-POSITIVE EVALUATION ---
    {
        "id": "fp_1",
        "lang": "mixed",
        "category": "legitimate",
        "text": "Kal office mein meeting hai, I'll join at 10.",
        "desc": "Benign code-switching 1"
    },
    {
        "id": "fp_2",
        "lang": "mixed",
        "category": "legitimate",
        "text": "Lunch ayitha? I'll call you later.",
        "desc": "Benign code-switching 2"
    },
    {
        "id": "fp_3",
        "lang": "mixed",
        "category": "legitimate",
        "text": "Aaj payment kar dena, okay?",
        "desc": "Benign code-switching 3"
    },
    # --- 6. URL SECURITY REGRESSION ---
    {
        "id": "url_reg_1",
        "lang": "mixed",
        "category": "malicious",
        "text": "Update account [Click Here](https://example.com/login?token=abc&user=xyz%20name)",
        "desc": "Markdown + long encoded query params"
    },
    {
        "id": "url_reg_2",
        "lang": "en",
        "category": "malicious",
        "text": "Login here: https://example.com/1 and here https://example.com/2",
        "desc": "Multiple URLs"
    }
]

print("=== RUNNING FULL AUDIT DATASET ===")
for test in audit_dataset:
    try:
        t0 = time.perf_counter()
        res = analyze_message(MessageRequest(message=test["text"]))
        t_ms = (time.perf_counter() - t0) * 1000
        
        mode = res.get("explainable_ai", {}).get("language_info", {}).get("language_mode", "unknown")
        pred = res["prediction"]
        risk = res["risk_score"]
        urls = res.get("explainable_ai", {}).get("url_analysis", [])
        url_count = len(urls)
        print(f"[{test['id']}] Expected: {test['category']:<10} | Pred: {pred:<10} | Mode: {mode:<10} | Risk: {risk:<6.2f} | URLs: {url_count} | Time: {t_ms:.1f}ms")
    except Exception as e:
        print(f"[{test['id']}] FAILED: {str(e)}")

print("\n=== EVALUATING TRANSLATION FAILURE + URL ===")
from unittest.mock import patch
with patch('backend.language_utils.get_translator') as mock_trans:
    mock_trans.side_effect = Exception('API Timeout')
    res = analyze_message(MessageRequest(message="NEW Tumhara bank khata band ho gaya hai: https://evil.com"))
    
    xai = res.get("explainable_ai", {})
    lang_info = xai.get("language_info", {})
    url_info = xai.get("url_analysis", [])
    print(f"Prediction: {res['prediction']} (Expected: review/scam)")
    print(f"Translation Status: {lang_info.get('translation_status')}")
    print(f"Analysis Status: {lang_info.get('analysis_status')}")
    print(f"Requires Manual Review: {lang_info.get('requires_manual_review')}")
    print(f"URL Extracted: {len(url_info) > 0}")

