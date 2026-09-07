import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

sys.path.append('backend')
from main import analyze_message, MessageRequest
from language_utils import process_multilingual
from risk_engine import analyze_scam_patterns
from semantic_analyzer import analyze_semantic_risk
import joblib

text = 'നിങ്ങളുടെ അക്കൗണ്ട് മരവിപ്പിച്ചു. ഉടൻ അപ്ഡേറ്റ് ചെയ്യുക'

processed, lang_meta = process_multilingual(text)
print('original text:', text.encode('utf-8'))
print('detected language:', lang_meta.get('detected_language'))
print('translation status:', lang_meta.get('translation_status'))
print('translated text:', processed.encode('utf-8'))

res = analyze_message(MessageRequest(message=text))
print('message model risk:', res['components'].get('message_risk', {}).get('risk_score'))
print('pattern risk:', res['components'].get('pattern_risk', {}).get('risk_score'))
print('url risk:', res.get('components', {}).get('url_risk', {}).get('risk_score'))
print('combined risk:', res['risk_score'])
print('classification:', res['prediction'])

