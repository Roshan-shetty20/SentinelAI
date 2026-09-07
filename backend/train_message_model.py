import os
import joblib
import pandas as pd
import re
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ============================================================
# PATHS
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "SMSSpamCollection")
LEGIT_PATH = os.path.join(BASE_DIR, "..", "data", "legitimate_messages.csv")
SCAM_PATH = os.path.join(BASE_DIR, "..", "data", "scam_messages.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# ============================================================
# LOAD DATASET
# ============================================================
print("Loading datasets...")
df_main = pd.read_csv(DATA_PATH, sep="\t", header=None, names=["label", "message"], encoding="utf-8")
df_legit = pd.read_csv(LEGIT_PATH)
df_scam = pd.read_csv(SCAM_PATH)

# Upsample custom datasets to ensure the model learns from them heavily
df = pd.concat([df_main, pd.concat([df_legit]*50, ignore_index=True), pd.concat([df_scam]*50, ignore_index=True)], ignore_index=True)

print(f"Total messages: {len(df)}")

df["label"] = df["label"].map({"ham": 0, "spam": 1})
df = df.dropna(subset=["label", "message"])

# ============================================================
# PREPROCESSING
# ============================================================
URL_PATTERN = re.compile(
    r'https?://'
    r'[A-Za-z0-9.-]+'
    r'\.[A-Za-z]{2,}'
    r'(?:/[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=%-]*)?'
    , re.IGNORECASE
)

def preprocess_message(text):
    text = str(text)
    # Replace URLs with a neutral token
    text = URL_PATTERN.sub(' [URL] ', text)
    # Remove markdown links syntax but keep the text
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 \2', text)
    return text.strip()

X = df["message"].apply(preprocess_message)
y = df["label"]

# ============================================================
# TRAIN / TEST SPLIT
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
print(f"Training messages: {len(X_train)}")
print(f"Testing messages: {len(X_test)}")

# ============================================================
# TF-IDF VECTORIZER
# ============================================================
print("\nCreating TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words=None, # DO NOT use English stop words for multilingual SMS
    ngram_range=(1, 3), # Capture phrases like "do not share", "recharge successful"
    max_features=20000,
    token_pattern=r"(?u)\b\w+\b|\[URL\]"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# ============================================================
# TRAIN MODEL
# ============================================================
print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train_tfidf, y_train)

# ============================================================
# THRESHOLD CALIBRATION
# ============================================================
print("\n============================================================")
print("THRESHOLD CALIBRATION")
print("============================================================")
y_pred_proba = model.predict_proba(X_test_tfidf)[:, 1] # Probability of spam (class 1)

for thresh in [0.5, 0.6, 0.7, 0.8, 0.9]:
    y_pred = (y_pred_proba >= thresh).astype(int)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    legit_recall = tn / (tn + fp) if (tn + fp) > 0 else 0
    spam_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    fp_rate = fp / (tn + fp) if (tn + fp) > 0 else 0
    print(f"Threshold {thresh:.2f} | Acc: {acc:.4f} | Legit Recall: {legit_recall:.4f} | Scam Recall: {spam_recall:.4f} | FP Rate: {fp_rate:.4f}")

# Choose 0.50 or 0.60 as default for prediction here, but the backend will handle thresholding.
y_pred_final = (y_pred_proba >= 0.50).astype(int)

# ============================================================
# EVALUATION
# ============================================================
print("\n============================================================")
print("MESSAGE SCAM MODEL RESULTS (Threshold 0.50)")
print("============================================================")
print(f"Accuracy: {accuracy_score(y_test, y_pred_final) * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_final, target_names=["Ham", "Spam"]))

model_path = os.path.join(MODEL_DIR, "message_model.pkl")
vectorizer_path = os.path.join(MODEL_DIR, "message_vectorizer.pkl")
joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)
print("Saved models successfully.")
