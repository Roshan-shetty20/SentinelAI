
import re

text = 'httpLLusps-redelivery-\nfees-track comLpost'
normalized = text

normalized = re.sub(r'([A-Za-z0-9-]+)-\s*\n\s*([A-Za-z0-9-]+)', r'\1-\2', normalized)
print('After joining lines:', normalized)

normalized = re.sub(r'\b(https?)\s*L+', r'\1://', normalized, flags=re.IGNORECASE)
print('After HTTP fix:', normalized)

normalized = re.sub(r'\b(com|org|net|in|co|gov|edu)L+', r'\1/', normalized, flags=re.IGNORECASE)
print('After L to slash:', normalized)

normalized = re.sub(r'([A-Za-z0-9-]+)\s+(com|org|net|in|co|gov|edu)\b', r'\1.\2', normalized, flags=re.IGNORECASE)
print('After space to dot:', normalized)

url_pattern = r'https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=%-]*)?'
matches = re.findall(url_pattern, normalized, flags=re.IGNORECASE)
print('Matches:', matches)

