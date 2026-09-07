import re

texts = [
    'https://example.com)',
    'https://example.com].',
    'https://example.com,',
    '[visit](https://example.com/path?a=b&c=d)',
    'raw https://example.com/login',
    'https://example.com.',
    'https://example.com/a/b/c?x=1&y=2)'
]

def extract_urls(text):
    URL_PATTERN = re.compile(r'(https?://[^\s<>\"\'\[\]]+|www\.[^\s<>\"\'\[\]]+)', re.IGNORECASE)
    matches = URL_PATTERN.findall(text)
    clean_urls = []
    for m in matches:
        m = re.sub(r'[,.)]+$', '', m)
        clean_urls.append(m)
    return clean_urls

for t in texts:
    print(f'{t} -> {extract_urls(t)}')
