import json
import re

stopwords = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "please", "click", "update", "account", "verify", "link", "here"])

with open('eval_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

for item in dataset:
    text = item['text']
    text_clean = re.sub(r'https?://\S+', '', text)
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text_clean)]
    if not words: continue
    
    stop_count = sum(1 for w in words if w in stopwords)
    ratio = stop_count / len(words)
    print(f"{item['lang']:6s} | {ratio:.2f} ({stop_count}/{len(words)}) | {text_clean}")

