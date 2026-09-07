import json
import sys
sys.path.append('backend')
from main import analyze_message, MessageRequest, message_model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from unittest.mock import patch

message_model.multi_class = 'ovr'

with open('adversarial_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

print("=== EVALUATING MIXED-LANGUAGE ADVERSARIAL DATASET ===")
results = []
y_true = []
y_pred = []

for row in dataset:
    text = row["text"]
    expected = row["category"]
    
    # 1. Test New Architecture
    res = analyze_message(MessageRequest(message=text))
    mode = res.get("explainable_ai", {}).get("language_info", {}).get("language_mode", "unknown")
    pred = "scam" if res["prediction"] in ["suspicious", "scam"] else "safe"
    y_true.append(1 if expected in ["suspicious", "scam", "malicious"] else 0)
    y_pred.append(1 if pred == "scam" else 0)
    print(f"[{row['id']}] Mode: {mode:<12} | Pred: {pred:<5} | Expected: {expected}")
    
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
print(f"\\nAdversarial Dataset N={len(dataset)} | Acc: {acc:.3f} | Prec: {prec:.3f} | Rec: {rec:.3f}")
