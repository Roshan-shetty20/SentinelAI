import sys
sys.path.append('backend')
from main import sanitize_url_for_ml, url_vectorizer, url_model
import numpy as np

url = 'https://phon.pe/jiol'
sanitized_url = sanitize_url_for_ml(url)
print("Sanitized:", sanitized_url)

url_vector = url_vectorizer.transform([sanitized_url])
vocab = url_vectorizer.vocabulary_
inv_vocab = {v: k for k, v in vocab.items()}

indices = url_vector.nonzero()[1]
print("Features for this URL:")
for idx in indices:
    print(f"Token: {inv_vocab[idx]}, TF-IDF: {url_vector[0, idx]}")

probs = url_model.predict_proba(url_vector)[0]
print("Classes:", url_model.classes_)
print("Probs:", probs)

# Let's see the most important features driving it to class 0 (Phishing)
coef = url_model.coef_[0]
for idx in indices:
    print(f"Token '{inv_vocab[idx]}' coef: {coef[idx]}")

print("Intercept:", url_model.intercept_)

