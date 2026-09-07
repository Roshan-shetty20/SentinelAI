import sys
sys.path.append('backend')
from feature_extractor import URLFeatureExtractor
import pickle

with open('backend/url_model.pkl', 'rb') as f:
    model = pickle.load(f)

url = 'https://phon.pe/jiol'
extractor = URLFeatureExtractor()
features = extractor.extract(url)

print("URL:", url)
for k, v in features.items():
    print(f"{k}: {v}")

prob = model.predict_proba([list(features.values())])[0][1]
print("Probability of Phishing:", prob * 100)
