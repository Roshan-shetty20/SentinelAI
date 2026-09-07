import re
pattern = r'(https?://[^\s<>\"\'\[\]]+)'
print("Raw Python string pattern:", repr(pattern))
regex = re.compile(pattern)
print("Regex pattern:", repr(regex.pattern))
print("Match:", regex.findall('https://example.com/login'))

import sys
sys.path.append('backend')
import risk_engine
print("Risk engine pattern:", repr(risk_engine.URL_PATTERN.pattern))
print("Risk engine match:", risk_engine.URL_PATTERN.findall('https://example.com/login'))
