import sys
sys.path.append('.')
import main
from pydantic import BaseModel
import warnings
warnings.filterwarnings('ignore')

class Req(BaseModel):
    message: str

main.message_model_loaded = True
main.url_model_loaded = True
main.url_model = main.joblib.load(main.URL_MODEL_PATH)
main.url_vectorizer = main.joblib.load(main.URL_VECTORIZER_PATH)
main.message_model = main.joblib.load(main.MESSAGE_MODEL_PATH)
main.message_vectorizer = main.joblib.load(main.MESSAGE_VECTORIZER_PATH)

main.message_model.multi_class = 'ovr'
main.url_model.multi_class = 'ovr'

msgs = [
    'https://www.google.com',
    '[Sign in to your account](https://www.google.com)',
    '[Sign in to your account](https://login.microsoftonline.com/example/path)',
    'Your account information was updated.',
    '???? ???? ??????? ????? ?? ?? ?? ???'
]

for m in msgs:
    print(f'--- {m} ---')
    try:
        res = main.analyze_message(Req(message=m))
        print(f"Risk: {res.get('final_risk_score', 'N/A')}, Pred: {res.get('prediction', 'N/A')}")
        print(f"Components: {res.get('components', {})}")
        # print("Pattern result from risk engine: ", res.get("model_3", {})) # We can't access model_3 directly from response if it's not exported, but it's in components
    except Exception as e:
        print(f"Error: {e}")
    print()
