import sys
sys.path.append('backend')
from backend.main import remove_markdown_links
import backend.risk_engine as risk_engine
import json

tests = [
    {"name": "Raw URL", "input": "https://example.com/login"},
    {"name": "Markdown URL", "input": "[Sign in](https://example.com/login)"},
    {"name": "Multiple Markdown URLs", "input": "Visit [Google](https://google.com) and [GitHub](https://github.com)."},
    {"name": "Long query strings", "input": "[View](https://example.com/page?id=1234567890abcdef)"},
    {"name": "Encoded parameters", "input": "[Login](https://example.com/login?u=user%40email.com&b=%2Fpath)"},
    {"name": "Trailing )", "input": "Check this link (https://example.com)"},
    {"name": "Trailing .", "input": "Go to https://example.com."},
    {"name": "Trailing ,", "input": "If you visit https://example.com, you will see it."},
    {"name": "URL inside surrounding text", "input": "Please visit https://example.com to verify your account."},
    {"name": "Mixed Markdown and raw URLs", "input": "Go to [Portal](https://portal.com) or just visit https://example.com"},
    {"name": "Enterprise auth URL (A)", "input": "https://example.com/login?SAMLRequest=longdummy1234&RelayState=abcxyz"},
    {"name": "Enterprise auth URL (B)", "input": "[Sign in](https://example.com/login?SAMLRequest=longdummy1234&RelayState=abcxyz)"}
]

for t in tests:
    print(f"=== TEST: {t['name']} ===")
    print(f"INPUT: {t['input']}")
    
    # Text sent to Message Model
    clean_text = remove_markdown_links(t['input'])
    print(f"TEXT SENT TO MESSAGE MODEL: {clean_text}")
    
    # URL extraction
    pattern_result = risk_engine.analyze_scam_patterns(t['input'])
    extracted_urls = pattern_result.get('detected_urls', [])
    
    # We didn't explicitly return anchor from main.py's helper as it was just a replacement helper, 
    # but we can show it here for the log.
    import re
    md_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\s<>\"\\'\[\]]+|www\.[^\s<>\"\\'\[\]]+)\)', re.IGNORECASE)
    anchors = []
    urls = []
    for match in md_pattern.finditer(t['input']):
        anchors.append(match.group(1).strip())
        u = match.group(2).strip()
        u = re.sub(r'[,.)\]]+$', '', u)
        urls.append(u)
    
    if anchors:
        print(f"EXTRACTED ANCHOR: {anchors}")
    else:
        print("EXTRACTED ANCHOR: None")
        
    print(f"EXTRACTED URL: {extracted_urls}")
    print(f"URL SENT TO URL MODEL: {extracted_urls}")
    print()

