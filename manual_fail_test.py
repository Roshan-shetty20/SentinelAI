import sys
sys.path.append('backend')
from backend.main import analyze_message
from backend.models import MessageRequest
from unittest.mock import patch
from language_utils import process_multilingual

print("Testing English")
req = MessageRequest(message="Your bank account is suspended.")
res = analyze_message(req)
print("Eng Result:", res['prediction'], res['risk_score'])

print("Testing Hindi with Timeout")
with patch('backend.language_utils.get_translator') as mock_trans:
    mock_trans.side_effect = Exception("API Timeout")
    
    req2 = MessageRequest(message="तत्काल! आपका बैंक खाता निलंबित कर दिया गया है। तुरंत क्लिक करें।")
    res2 = analyze_message(req2)
    print("Hindi Fallback Result:", res2['prediction'], res2['risk_score'])
    print("Hindi XAI:", res2['explanation']['language_info'])
