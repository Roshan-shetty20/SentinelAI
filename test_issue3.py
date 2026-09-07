import sys
sys.path.append('backend')
from main import analyze_message, MessageRequest
res = analyze_message(MessageRequest(message='[https://www.google.com](https://www.google.com)'))
print('Final Risk:', res['risk_score'])
print('Components:', res['components'])
