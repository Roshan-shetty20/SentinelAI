import re

def extract_markdown_links(text):
    md_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\s<>\"\'\[\]]+|www\.[^\s<>\"\'\[\]]+)\)', re.IGNORECASE)
    clean_text = text
    for match in md_pattern.finditer(text):
        anchor = match.group(1).strip()
        url = match.group(2).strip()
        url = re.sub(r'[,.)\]]+$', '', url)
        clean_text = clean_text.replace(match.group(0), anchor)
    return clean_text

print(extract_markdown_links('Please [Sign in to your account](https://example.com/login) to continue.'))
print(extract_markdown_links('raw https://example.com/login'))
print(extract_markdown_links('Here is [link1](https://example.com) and [link2](https://google.com)'))
