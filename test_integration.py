# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append('backend')
from backend.main import message_model, message_vectorizer, remove_markdown_links
from backend.risk_engine import analyze_scam_patterns
from backend.combined_risk_engine import calculate_combined_risk
from backend.language_utils import process_multilingual

message_model.multi_class = 'ovr'

texts = {
    "English": "Your account information was updated.",
    "Hindi": "आपकी खाता जानकारी अपडेट कर दी गई है।",
    "Kannada": "ನಿಮ್ಮ ಖಾತೆ ಮಾಹಿತಿಯನ್ನು ನವೀಕರಿಸಲಾಗಿದೆ.",
    "Tamil": "உங்கள் கணக்கு தகவல் புதுப்பிக்கப்பட்டது.",
    "Telugu": "మీ ఖాతా సమాచారం నవీకరించబడింది.",
    "Malayalam": "നിങ്ങളുടെ അക്കൗണ്ട് വിവരങ്ങൾ അപ്ഡേറ്റ് ചെയ്തു.",
    "Marathi": "तुमची खाते माहिती अद्यतनित केली गेली आहे.",
    "Bengali": "আপনার অ্যাকাউন্ট তথ্য আপডেট করা হয়েছে।",
    "Arabic": "تم تحديث معلومات حسابك.",
    "Spanish": "La información de su cuenta ha sido actualizada.",
    
    "Hindi + English": "आपका account information update किया गया है।",
    "Kannada + English": "ನಿಮ್ಮ account information update ಮಾಡಲಾಗಿದೆ.",
    "Tamil + English": "உங்கள் account information update செய்யப்பட்டது.",
    "Telugu + English": "మీ account information update చేయబడింది.",
    
    "Hindi Markdown": "आपका खाता अपडेट किया गया है। [Sign in](https://example.com/login)",
    "English Markdown": "Your account has been updated. [Sign in](https://example.com/login)"
}

print("--- MULTILINGUAL INTEGRATION TEST ---\n")
for name, txt in texts.items():
    print(f"[{name}] Input: {txt}")
    
    processed, meta = process_multilingual(txt)
    print(f"Translated output: {processed}")
    print(f"Meta: {meta}")
    
    clean = remove_markdown_links(processed)
    
    vec = message_vectorizer.transform([clean])
    prob = message_model.predict_proba(vec)[0]
    classes = list(message_model.classes_)
    idx = classes.index(message_model.predict(vec)[0])
    conf = float(prob[idx] * 100)
    msg_risk = conf if classes[idx] == 1 else (100 - conf)
    
    pat_res = analyze_scam_patterns(processed)
    pat_risk = float(pat_res.get("pattern_risk_score", 0))
    urls = pat_res.get("detected_urls", [])
    
    comb = calculate_combined_risk(message_risk=msg_risk, semantic_risk=0, pattern_risk=pat_risk, credential_signal=False)
    
    print(f"Message Risk: {msg_risk:.2f} | Pattern Risk: {pat_risk:.2f} | Extracted URLs: {urls}")
    print(f"Final Class: {comb['prediction']} (Risk: {comb['final_risk_score']:.2f})\n")

