import sys
sys.path.append('backend')
from backend.main import remove_markdown_links, message_model, message_vectorizer, url_model, url_vectorizer, analyze_semantic_risk
import backend.risk_engine as risk_engine
from backend.combined_risk_engine import calculate_combined_risk

import joblib

# Ensure models are 'ovr' patched for prediction
message_model.multi_class = 'ovr'
url_model.multi_class = 'ovr'

tests = [
    # Group 1
    "https://example.com/login",
    "[Sign in](https://example.com/login)",
    "[Sign in to your account](https://example.com/login)",
    "[Login](https://example.com/login)",
    "[Continue](https://example.com/login)",
    "[Open website](https://example.com/login)",
    # Group 2
    "[Sign in](https://example.com/account)",
    "[Sign in](https://example.com/security)",
    "[Sign in](https://example.com/random-path)",
    # Group 3
    "[Sign in to your account](https://example.com/login?SAMLRequest=dummy&RelayState=dummy)",
    "[Access your account](https://example.com/auth?redirect=dummy&state=dummy)",
    "[View document](https://example.com/document?id=12345&token=dummy)",
    # Group 4
    "Sign in to your account",
    "[Sign in to your account](https://example.com/login)",
    # Group 5
    "Please sign in to your account.",
    "Please [sign in to your account](https://example.com/login).",
    "You can access the portal here: [Sign in](https://example.com/login)."
]

for t in tests:
    print(f"==================================================")
    print(f"INPUT: {t}")
    
    clean_text = remove_markdown_links(t)
    print(f"CLEANED MESSAGE: {clean_text}")
    
    # 1. Message Risk
    vec_msg = message_vectorizer.transform([clean_text])
    msg_prob = message_model.predict_proba(vec_msg)[0]
    classes = list(message_model.classes_)
    idx = classes.index(message_model.predict(vec_msg)[0])
    msg_confidence = float(msg_prob[idx] * 100)
    if classes[idx] == 1:
        msg_risk = msg_confidence
    else:
        msg_risk = 100 - msg_confidence
        
    print(f"MESSAGE MODEL RISK: {msg_risk:.2f}")
    
    # 2. Pattern Risk
    pattern_res = risk_engine.analyze_scam_patterns(t)
    pattern_risk = float(pattern_res.get("pattern_risk_score", 0))
    urls = pattern_res.get("detected_urls", [])
    print(f"EXTRACTED URLS: {urls}")
    print(f"PATTERN MODEL RISK: {pattern_risk:.2f}")
    
    # 3. URL Risk
    url_risk = None
    if urls:
        max_url_risk = 0
        for u in urls:
            u_vec = url_vectorizer.transform([u])
            u_prob = url_model.predict_proba(u_vec)[0]
            u_classes = list(url_model.classes_)
            u_idx = u_classes.index(url_model.predict(u_vec)[0])
            u_conf = float(u_prob[u_idx] * 100)
            u_r = u_conf if u_classes[u_idx] == 1 else (100 - u_conf)
            if u_r > max_url_risk:
                max_url_risk = u_r
        url_risk = max_url_risk
    print(f"URL MODEL RISK: {url_risk if url_risk is not None else 'N/A'}")
    
    # Semantic Risk (Optional but good for combined)
    sem_res = analyze_semantic_risk(clean_text)
    sem_risk = float(sem_res.get("semantic_risk_score", 0))
    
    # Combined Risk
    comb_res = calculate_combined_risk(
        message_risk=msg_risk,
        semantic_risk=sem_risk,
        pattern_risk=pattern_risk,
        url_risk=url_risk,
        credential_signal=any(s.get("type") == "credential_request" for s in pattern_res.get("signals", []))
    )
    
    print(f"FINAL RISK SCORE: {comb_res['final_risk_score']:.2f}")
    print(f"FINAL CLASSIFICATION: {comb_res['prediction']}")
