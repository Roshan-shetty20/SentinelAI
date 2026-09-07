import sys
sys.path.append('backend')
from main import evaluate_url_ml
import json

res = evaluate_url_ml("https://example.com/product?utm_source=test&utm_campaign=test")
print(json.dumps(res, indent=2))
