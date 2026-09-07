import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import warnings
import os
from main import sanitize_url_for_ml

warnings.filterwarnings('ignore')

# 1. Load Original Dataset
print("Loading PhiUSIIL dataset...")
df_main = pd.read_csv('data/PhiUSIIL_Phishing_URL_Dataset.csv', usecols=['URL', 'label'])

# 2. Load Hard Negatives
print("Loading Hard Negatives...")
df_hard = pd.read_csv('data/legitimate_hard_negatives.csv')
df_short = pd.read_csv('data/short_urls2.csv')

# Combine
df_hard_upsampled = pd.concat([df_hard] * 500, ignore_index=True)
df_short_upsampled = pd.concat([df_short] * 200, ignore_index=True)
df = pd.concat([df_main, df_hard_upsampled, df_short_upsampled], ignore_index=True)

# Apply Sanitization BEFORE training! (Critical to avoid train/inference mismatch)
print("Sanitizing URLs...")
df['URL'] = df['URL'].astype(str).apply(sanitize_url_for_ml)

# 3. Features & Labels
X = df['URL']
y = df['label'].astype(int)

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training set size:", len(X_train))
print("Test set size:", len(X_test))

# 5. Pipeline Setup
print("Fitting TF-IDF Vectorizer...")
vectorizer = TfidfVectorizer(
    analyzer='char',
    ngram_range=(2, 5),
    min_df=2,
    max_features=100000,
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training Logistic Regression Model...")
model = LogisticRegression(
    max_iter=1000,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train_vec, y_train)

# 6. Evaluation & Threshold Selection
print("Evaluating default threshold (0.5)...")
y_pred_proba = model.predict_proba(X_test_vec)
phishing_index = list(model.classes_).index(0)

# Evaluate threshold
thresholds = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
for thresh in thresholds:
    y_pred_thresh = np.where(y_pred_proba[:, phishing_index] >= thresh, 0, 1)
    
    acc = accuracy_score(y_test, y_pred_thresh)
    rec_phish = recall_score(y_test, y_pred_thresh, pos_label=0)
    rec_legit = recall_score(y_test, y_pred_thresh, pos_label=1)
    prec_phish = precision_score(y_test, y_pred_thresh, pos_label=0)
    
    print(f"Threshold: {thresh:.2f} | Acc: {acc:.4f} | Phish Recall: {rec_phish:.4f} | Legit Recall: {rec_legit:.4f} | Phish Prec: {prec_phish:.4f}")

# 7. Save Models
os.makedirs('backend/models', exist_ok=True)
joblib.dump(vectorizer, 'backend/models/url_tfidf_vectorizer.pkl')
joblib.dump(model, 'backend/models/url_tfidf_model.pkl')

print("Saved models successfully.")
