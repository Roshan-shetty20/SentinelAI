import sys, os, joblib, json, re
sys.path.append('backend')
import backend.main as main
from backend.main import MessageRequest
import backend.risk_engine as risk_engine

main.message_model_loaded = True
main.url_model_loaded = True
main.url_model = joblib.load(main.URL_MODEL_PATH)
main.url_vectorizer = joblib.load(main.URL_VECTORIZER_PATH)
main.message_model = joblib.load(main.MESSAGE_MODEL_PATH)
main.message_vectorizer = joblib.load(main.MESSAGE_VECTORIZER_PATH)
main.message_model.multi_class = 'ovr'
main.url_model.multi_class = 'ovr'

test_cases_1 = [
    ('Raw URL', 'https://example.com'),
    ('Basic MD', '[Example](https://example.com)'),
    ('Visit MD', '[Visit website](https://example.com)'),
    ('Sign in MD', '[Sign in to your account](https://example.com/login)'),
    ('Document MD', '[View document](https://example.com/document?id=123)'),
    ('Open token MD', '[Open](https://example.com/path?token=abc123)'),
    ('Query MD', '[Open link](https://example.com/a/b/c?x=1&y=2)'),
    ('Multiple MD', 'Here is [link1](https://example.com) and [link2](https://example.com)'),
    ('Mixed text MD', 'Please click [here](https://example.com) to login.'),
    ('URL encoded MD', '[Login](https://example.com/login?u=user%40email.com)'),
]

results = {}

for name, text in test_cases_1:
    res = main.analyze_message(MessageRequest(message=text))
    # Extract URLs natively through risk_engine
    pattern_res = risk_engine.analyze_scam_patterns(text)
    extracted_urls = pattern_res.get('detected_urls', [])
    
    # Check what features message_vectorizer sees
    msg_vec = main.message_vectorizer.transform([text])
    msg_features = [main.message_vectorizer.get_feature_names_out()[i] for i in msg_vec.nonzero()[1]]
    
    # Check what features url_vectorizer sees for the first extracted URL (if any)
    url_features = []
    if extracted_urls:
        url_vec = main.url_vectorizer.transform([extracted_urls[0]])
        url_features = [main.url_vectorizer.get_feature_names_out()[i] for i in url_vec.nonzero()[1]]
    
    results[name] = {
        'input': text,
        'extracted_urls': extracted_urls,
        'extracted_anchor': None, # Since there's no MD parser, this is None!
        'normalized_url': extracted_urls[0] if extracted_urls else None, # no real normalization
        'text_features': msg_features[:10],
        'url_features': url_features[:10],
        'prediction': res['prediction'],
        'risk_score': res['final_risk_score']
    }

print(json.dumps(results, indent=2))
