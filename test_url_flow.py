import sys
sys.path.append('backend')
from main import evaluate_url_ml

url_eval = evaluate_url_ml("https://phon.pe/jiol")
print(url_eval)
