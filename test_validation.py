# -*- coding: utf-8 -*-
import sys
import io
import time
from unittest.mock import patch
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append('backend')
from backend.main import message_model, message_vectorizer, remove_markdown_links
from backend.risk_engine import analyze_scam_patterns, URL_PATTERN
from backend.combined_risk_engine import calculate_combined_risk
from backend.language_utils import (
    process_multilingual, protect_sensitive_tokens, detect_language, 
    translate_to_english, restore_sensitive_tokens
)

message_model.multi_class = 'ovr'

def run_risk(processed, meta):
    clean = remove_markdown_links(processed)
    vec = message_vectorizer.transform([clean])
    prob = message_model.predict_proba(vec)[0]
    classes = list(message_model.classes_)
    idx = classes.index(message_model.predict(vec)[0])
    conf = float(prob[idx] * 100)
    msg_risk = conf if classes[idx] == 1 else (100 - conf)
    pat_res = analyze_scam_patterns(processed)
    pat_risk = float(pat_res.get("pattern_risk_score", 0))
    comb = calculate_combined_risk(message_risk=msg_risk, semantic_risk=0, pattern_risk=pat_risk, credential_signal=False, requires_manual_review=meta.get("requires_manual_review", False))
    return msg_risk, pat_risk, comb['final_risk_score']

print("=== 1. SHOW ACTUAL TRANSLATIONS ===")
texts_1 = {
    "Hindi": "मैंने कल बैंक में 500 रुपये जमा किए।",
    "Kannada": "ನಾನು ನಿನ್ನೆ ಬ್ಯಾಂಕ್‌ಗೆ 500 ರೂಪಾಯಿ ಜಮಾ ಮಾಡಿದ್ದೇನೆ.",
    "Tamil": "நான் நேற்று வங்கியில் 500 ரூபாய் செலுத்தினேன்.",
    "Telugu": "నేను నిన్న బ్యాంకులో 500 రూపాయలు జమ చేసాను.",
    "Malayalam": "ഞാൻ ഇന്നലെ ബാങ്കിൽ 500 രൂപ നിക്ഷേപിച്ചു.",
    "Marathi": "मी काल बँकेत 500 रुपये जमा केले.",
    "Bengali": "আমি গতকাল ব্যাংকে ৫০০ টাকা জমা করেছি।",
    "Arabic": "أودعت 500 روبية في البنك أمس.",
    "Spanish": "Ayer deposité 500 rupias en el banco."
}
for lang, txt in texts_1.items():
    processed, meta = process_multilingual(txt)
    m_risk, p_risk, f_risk = run_risk(processed, meta)
    print(f"Original: {txt}")
    print(f"Detected language: {meta['detected_language']}")
    print(f"Detection confidence: {meta['confidence']:.4f}")
    print(f"Translated text: {processed}")
    print(f"Translation successful: {meta.get('translation_status')}")
    print(f"Message Model risk: {m_risk:.2f}")
    print(f"Pattern risk: {p_risk:.2f}")
    print(f"Final risk: {f_risk:.2f}\n")


print("=== 2. SEMANTIC PRESERVATION ===")
# Testing negation and dates
text_2 = "La reunión no es el 12 de octubre."
processed_2, meta_2 = process_multilingual(text_2)
print(f"Original: {text_2}")
print(f"Translated: {processed_2}\n")


print("=== 3. PROTECTED TOKEN VALIDATION ===")
text_3 = "El código es 987654. Email: test@example.com. Tel: +1-800-555-1234. [Doc](https://example.com/path?id=123)"
protected_text, mapping = protect_sensitive_tokens(text_3)
processed_3, meta_3 = process_multilingual(text_3)
print(f"Original: {text_3}")
print(f"Protected (before translation): {protected_text}")
print(f"Mapping: {mapping}")
print(f"Final Restored: {processed_3}\n")


print("=== 4. MARKDOWN + MULTILINGUAL ===")
text_4 = "आपका खाता अपडेट किया गया है। [Sign in](https://example.com/login)"
print(f"Original Input: {text_4}")
p_txt, m_map = protect_sensitive_tokens(text_4)
print(f"URL protection: {p_txt}")
lang_info = detect_language(p_txt.replace('__URL_0__', ''))
print(f"Language detection: {lang_info}")
t_txt = translate_to_english(p_txt)
print(f"Translation: {t_txt}")
r_txt = restore_sensitive_tokens(t_txt, m_map)
print(f"URL restoration: {r_txt}")
c_txt = remove_markdown_links(r_txt)
print(f"Markdown cleaning: {c_txt}\n")


print("=== 5. MIXED-LANGUAGE TEST ===")
texts_5 = {
    "English + Hindi": "आपका account information update किया गया है।",
    "English + Kannada": "ನಿಮ್ಮ account information update ಮಾಡಲಾಗಿದೆ.",
    "English + Tamil": "உங்கள் account information update செய்யப்பட்டது.",
    "English + Telugu": "మీ account information update చేయబడింది.",
    "English + Malayalam": "നിങ്ങളുടെ account information update ചെയ്തു.",
    "English + Spanish": "La account information ha sido update."
}
for name, txt in texts_5.items():
    processed, meta = process_multilingual(txt)
    m_risk, p_risk, f_risk = run_risk(processed, meta)
    print(f"Detected language: {meta['detected_language']}")
    print(f"Detection confidence: {meta['confidence']:.4f}")
    print(f"Original text: {txt}")
    print(f"Translated text: {processed}")
    print(f"Translation applied?: {meta.get('translation_status')}")
    print(f"Message risk: {m_risk:.2f}")
    print(f"Pattern risk: {p_risk:.2f}")
    print(f"Final risk: {f_risk:.2f}\n")


print("=== 6. TRANSLATION FAILURE TEST ===")
with patch('backend.language_utils.get_translator') as mock_trans:
    mock_trans.side_effect = Exception("HTTP 500 Internal Server Error")
    processed_6, meta_6 = process_multilingual("यह एक परीक्षण है।")
    m_risk, p_risk, f_risk = run_risk(processed_6, meta_6)
    print(f"Fallback text: {processed_6}")
    print(f"Message risk: {m_risk:.2f}")
    print(f"Final risk: {f_risk:.2f}")
    print(f"Translation status: {meta_6.get('translation_status')} (Error: {meta_6['error']})")
    print(f"XAI metadata: {meta_6}\n")

print("=== 7. FALSE NEGATIVE SECURITY CHECK ===")
# Use an urgent message in Hindi that would be flagged if English
urgent_hi = "तत्काल! आपका बैंक खाता निलंबित कर दिया गया है। तुरंत क्लिक करें।"
with patch('backend.language_utils.get_translator') as mock_trans:
    mock_trans.side_effect = Exception("API Timeout")
    processed_7, meta_7 = process_multilingual(urgent_hi)
    m_risk, p_risk, f_risk = run_risk(processed_7, meta_7)
    print(f"Failed translation fallback: {processed_7}")
    print(f"Message Risk on fallback: {m_risk:.2f}")
    print(f"Pattern Risk on fallback: {p_risk:.2f}")
    print(f"Final Risk: {f_risk:.2f}\n")

print("=== 8. PERFORMANCE ===")
def measure(func, *args, iters=10):
    start = time.perf_counter()
    for _ in range(iters):
        func(*args)
    return ((time.perf_counter() - start) / iters) * 1000

lat_en_det = measure(detect_language, "Hello this is English")
lat_en_full = measure(process_multilingual, "Hello this is English")
lat_es_det = measure(detect_language, "Hola esto es español")

# Disable cache for translation measurement
import backend.language_utils as lu
lu._translation_cache.clear()
lat_es_trans = measure(lu.translate_to_english, "Hola esto es español", iters=3)
lu._translation_cache.clear()
lat_es_full = measure(process_multilingual, "Hola esto es español", iters=3)

# Cached
lu.process_multilingual("Hola esto es español") # prime cache
lat_es_cached = measure(process_multilingual, "Hola esto es español")

print(f"English detection latency: {lat_en_det:.2f} ms")
print(f"English complete analysis latency: {lat_en_full:.2f} ms")
print(f"Non-English detection latency: {lat_es_det:.2f} ms")
print(f"Translation latency: {lat_es_trans:.2f} ms")
print(f"Non-English complete analysis latency: {lat_es_full:.2f} ms")
print(f"Cached translation latency: {lat_es_cached:.2f} ms\n")

