import re
import backend.risk_engine as risk_engine

print(risk_engine.URL_PATTERN.findall('https://example.com/login'))
