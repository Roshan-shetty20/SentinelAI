# -*- coding: utf-8 -*-
import sys
sys.path.append('backend')
from backend.main import message_model, message_vectorizer, remove_markdown_links
from backend.risk_engine import analyze_scam_patterns
from backend.combined_risk_engine import calculate_combined_risk

message_model.multi_class = 'ovr'

vocab = message_vectorizer.vocabulary_
print(f"Vocab Size: {len(vocab)}")
non_ascii_words = [w for w in vocab if not w.isascii()]
print(f"Non-ASCII words in vocab: {len(non_ascii_words)}")

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
    "Spanish": "La información de su cuenta ha sido actualizada."
}

print("\n--- MULTILINGUAL TESTS ---")
for lang, txt in texts.items():
    clean = remove_markdown_links(txt)
    vec = message_vectorizer.transform([clean])
    analyzer = message_vectorizer.build_analyzer()
    tokens = analyzer(clean)
    recognized = [t for t in tokens if t in vocab]
    unknown = [t for t in tokens if t not in vocab]
    
    nz = vec.nnz
    dim = vec.shape[1]
    
    prob = message_model.predict_proba(vec)[0]
    classes = list(message_model.classes_)
    idx = classes.index(message_model.predict(vec)[0])
    conf = float(prob[idx] * 100)
    msg_risk = conf if classes[idx] == 1 else (100 - conf)
    
    sem_risk = 0
    pat_res = analyze_scam_patterns(clean)
    pat_risk = pat_res.get("pattern_risk_score", 0)
    comb = calculate_combined_risk(message_risk=msg_risk, semantic_risk=sem_risk, pattern_risk=pat_risk, credential_signal=False)
    
    print(f"\nLanguage: {lang}")
    print(f"Input: {txt}")
    print(f"Chars: {len(txt)} | Tokens: {len(tokens)} | Recognized: {len(recognized)} | Unknown: {len(unknown)}")
    if recognized:
        print(f"Recognized words: {recognized}")
    print(f"Vector Non-zero: {nz} | Dim: {dim}")
    print(f"Probabilities: {prob}")
    print(f"Message Risk: {msg_risk:.2f}")
    print(f"Final Class: {comb['prediction']} (Risk: {comb['final_risk_score']:.2f})")

mixed_texts = {
    "English": "Your account information was updated.",
    "Hindi + English": "आपका account information update किया गया है।",
    "Kannada + English": "ನಿಮ್ಮ account information update ಮಾಡಲಾಗಿದೆ.",
    "Tamil + English": "உங்கள் account information update செய்யப்பட்டது.",
    "Telugu + English": "మీ account information update చేయబడింది."
}

print("\n--- MIXED LANGUAGE TESTS ---")
for lang, txt in mixed_texts.items():
    clean = remove_markdown_links(txt)
    vec = message_vectorizer.transform([clean])
    analyzer = message_vectorizer.build_analyzer()
    tokens = analyzer(clean)
    recognized = [t for t in tokens if t in vocab]
    
    nz = vec.nnz
    
    prob = message_model.predict_proba(vec)[0]
    classes = list(message_model.classes_)
    idx = classes.index(message_model.predict(vec)[0])
    conf = float(prob[idx] * 100)
    msg_risk = conf if classes[idx] == 1 else (100 - conf)
    
    print(f"\nLanguage: {lang}")
    print(f"Recognized words: {recognized}")
    print(f"Vector Non-zero: {nz}")
    print(f"Message Risk: {msg_risk:.2f}")
