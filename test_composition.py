import re
from langdetect import detect_langs

def analyze_composition(text):
    # Remove obvious non-words (this is a mock for the protection step)
    text = re.sub(r'https?://\S+', '', text)
    
    # Check for non-Latin characters. If dominant, it's non-English/mixed.
    # Actually let's just rely on langdetect chunking.
    words = re.findall(r'\b[a-zA-Z\u00C0-\u024F\u0400-\u04FF\u0600-\u06FF\u0900-\u097F]+\b', text)
    words = [w for w in words if len(w) > 1] # filter single letters
    
    if not words:
        return 'english', 1.0 # fallback
        
    chunk_size = 3
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(' '.join(words[i:i+chunk_size]))
        
    en_probs = []
    for chunk in chunks:
        if len(chunk) < 3: continue
        try:
            langs = {l.lang: l.prob for l in detect_langs(chunk)}
            en_probs.append(langs.get('en', 0.0))
        except:
            pass
            
    if not en_probs:
        try:
            langs = {l.lang: l.prob for l in detect_langs(text)}
            en_prob = langs.get('en', 0.0)
            en_probs = [en_prob]
        except:
            return 'english', 1.0
            
    avg_en = sum(en_probs) / len(en_probs)
    min_en = min(en_probs)
    max_en = max(en_probs)
    
    if avg_en > 0.8:
        if min_en < 0.3:
            mode = 'mixed'
        else:
            mode = 'english'
    elif avg_en < 0.2:
        if max_en > 0.7:
            mode = 'mixed'
        else:
            mode = 'non_english'
    else:
        mode = 'mixed'
        
    return mode, avg_en, en_probs

cases = [
    "Your account will be suspended. Verify immediately.",
    "आपका बैंक खाता बंद कर दिया जाएगा। तुरंत सत्यापन करें।",
    "Tumhara account suspend ho gaya hai, verify now.",
    "तुम्हारा बैंक खाता बंद हो गया है, अभी अपडेट करो।",
    "Tumhara bank khata block ho gaya hai, update karo.",
    "Kal meeting attend karna mat bhulna at 10 AM.",
    "Tumhara bank khata block ho gaya hai, update here: https://example.com/login"
]

for c in cases:
    mode, avg, probs = analyze_composition(c)
    print(f"[{mode:12s}] {avg:.2f} {probs} | {c}")
