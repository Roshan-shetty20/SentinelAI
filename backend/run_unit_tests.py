import sys
sys.path.append('.')
from main import remove_markdown_links
import risk_engine
import re

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

print("=== MARKDOWN EXTRACTION & URL PREPROCESSING UNIT TESTS ===\n")
for t in tests:
    print(f"TEST: {t['name']}")
    print(f"INPUT: {t['input']}")
    
    # 1. TEXT SENT TO MESSAGE MODEL
    clean_text = remove_markdown_links(t['input'])
    
    # 2. EXTRACTED URLS & ANCHORS
    md_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\s<>\"\'\[\]]+|www\.[^\s<>\"\'\[\]]+)\)', re.IGNORECASE)
    anchors = [m.group(1).strip() for m in md_pattern.finditer(t['input'])]
    
    # 3. URL SENT TO URL MODEL (via risk engine)
    pattern_result = risk_engine.analyze_scam_patterns(t['input'])
    extracted_urls = pattern_result.get('detected_urls', [])
    
    print(f"-> EXTRACTED ANCHOR: {anchors if anchors else 'None'}")
    print(f"-> EXTRACTED URL: {extracted_urls}")
    print(f"-> URL SENT TO URL MODEL: {extracted_urls}")
    print(f"-> TEXT SENT TO MESSAGE MODEL: {clean_text}")
    print("-" * 50)
