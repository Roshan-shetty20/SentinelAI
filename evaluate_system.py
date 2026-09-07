import json
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from unittest.mock import patch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

sys.path.append('backend')
import backend.language_utils as lu
from backend.main import analyze_message, message_model
from backend.main import MessageRequest

# Patch scikit-learn version mismatch bug
message_model.multi_class = 'ovr'

with open('eval_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Monkey-patch timing metrics
timing_stats = {
    'det': [],
    'trans': [],
    'full_en': [],
    'full_non_en': []
}

orig_detect = lu.detect_language_composition
def timed_detect(*args, **kwargs):
    t0 = time.perf_counter()
    res = orig_detect(*args, **kwargs)
    timing_stats['det'].append((time.perf_counter() - t0) * 1000)
    return res
lu.detect_language_composition = timed_detect

orig_translate = lu.translate_to_english
def timed_translate(*args, **kwargs):
    t0 = time.perf_counter()
    res = orig_translate(*args, **kwargs)
    timing_stats['trans'].append((time.perf_counter() - t0) * 1000)
    return res
lu.translate_to_english = timed_translate

results = []

def run_eval(sim_fail=False):
    run_results = []
    # clear cache
    lu._translation_cache.clear()
    
    def do_eval():
        for item in dataset:
            t0 = time.perf_counter()
            req = MessageRequest(message=item['text'])
            res = analyze_message(req)
            dur = (time.perf_counter() - t0) * 1000
            
            # Record component timing if English vs Non-English
            if item['lang'] == 'en':
                timing_stats['full_en'].append(dur)
            else:
                timing_stats['full_non_en'].append(dur)
                
            pred_class = res['prediction']
            # Map predictions to binary
            true_bin = 1 if item['label'] == 'malicious' else 0
            pred_bin = 1 if pred_class in ['suspicious', 'scam', 'review'] else 0
            
            run_results.append({
                'id': item['id'],
                'text': item['text'],
                'lang': item['lang'],
                'type': item['type'],
                'true_label': item['label'],
                'pred_class': pred_class,
                'true_bin': true_bin,
                'pred_bin': pred_bin,
                'msg_risk': res['risk_score'],
                'xai': res.get('explainable_ai', {}).get('language_info', {})
            })
            
    if sim_fail:
        with patch('backend.language_utils.get_translator') as mock_trans:
            mock_trans.side_effect = Exception("API Timeout")
            do_eval()
    else:
        do_eval()
        
    return run_results

print("Running Standard Evaluation...")
res_std = run_eval(sim_fail=False)

print("Running Translation Failure Evaluation...")
res_fail = run_eval(sim_fail=True)

# Calculate metrics
def calc_metrics(results_list, filter_fn=None):
    filtered = [r for r in results_list if filter_fn(r)] if filter_fn else results_list
    if not filtered: return None
    y_true = [r['true_bin'] for r in filtered]
    y_pred = [r['pred_bin'] for r in filtered]
    
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0,0,0,0)
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    
    return {
        'n': len(filtered),
        'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1,
        'fpr': fpr, 'fnr': fnr, 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn
    }

print("\n--- ML METRICS (STANDARD RUN) ---")
metrics_all = calc_metrics(res_std)
print(f"Total N={metrics_all['n']} | Acc: {metrics_all['acc']:.3f} | Prec: {metrics_all['prec']:.3f} | Rec: {metrics_all['rec']:.3f} | F1: {metrics_all['f1']:.3f}")
print(f"FPR: {metrics_all['fpr']:.3f} | FNR: {metrics_all['fnr']:.3f} | FP: {metrics_all['fp']} | FN: {metrics_all['fn']}")

print("\n--- ML METRICS BY SEGMENT ---")
for lang in ['en', 'hi', 'mixed']:
    m = calc_metrics(res_std, lambda r: r['lang'] == lang)
    if m: print(f"Lang={lang} | N={m['n']} | Acc: {m['acc']:.3f} | FNR: {m['fnr']:.3f}")

m_md = calc_metrics(res_std, lambda r: r['type'] == 'markdown')
if m_md: print(f"Type=Markdown | N={m_md['n']} | Acc: {m_md['acc']:.3f} | FNR: {m_md['fnr']:.3f}")

print("\n--- FALSE NEGATIVES (STANDARD RUN) ---")
fns = [r for r in res_std if r['true_bin'] == 1 and r['pred_bin'] == 0]
for fn in fns:
    print(f"[{fn['id']}] {fn['text']} -> {fn['pred_class']} (Msg Risk: {fn['msg_risk']:.2f})")

print("\n--- FALSE POSITIVES (STANDARD RUN) ---")
fps = [r for r in res_std if r['true_bin'] == 0 and r['pred_bin'] == 1]
for fp in fps:
    print(f"[{fp['id']}] {fp['text']} -> {fp['pred_class']} (Msg Risk: {fp['msg_risk']:.2f})")

print("\n--- TRANSLATION FAILURE RUN METRICS ---")
metrics_fail = calc_metrics(res_fail)
print(f"Total N={metrics_fail['n']} | Acc: {metrics_fail['acc']:.3f} | Prec: {metrics_fail['prec']:.3f} | Rec: {metrics_fail['rec']:.3f}")
print(f"FPR: {metrics_fail['fpr']:.3f} | FNR: {metrics_fail['fnr']:.3f} | FP: {metrics_fail['fp']} | FN: {metrics_fail['fn']}")

print("\n--- TRANSLATION FAILURE OVERVIEW ---")
fails = [r for r in res_fail if r['lang'] != 'en' and r['xai']['translation_status'] == 'failed']
print(f"Simulated failures caught: {len(fails)}")
for f in fails[:3]: # show 3 examples
    print(f"[{f['id']}] Class: {f['pred_class']} | Rev_Req: {f['xai']['requires_manual_review']}")


print("\n--- PERFORMANCE ---")
import numpy as np
def report_perf(name, arr):
    if not arr: return
    avg, med, p95, p99 = np.mean(arr), np.median(arr), np.percentile(arr, 95), np.percentile(arr, 99)
    print(f"{name:25s}: Avg={avg:.2f}ms | Med={med:.2f}ms | P95={p95:.2f}ms | P99={p99:.2f}ms")

report_perf("Lang Detection", timing_stats['det'])
report_perf("Translation", timing_stats['trans'])
report_perf("Complete (English)", timing_stats['full_en'])
report_perf("Complete (Non-English)", timing_stats['full_non_en'])

