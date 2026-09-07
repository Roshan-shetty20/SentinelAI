import sys
sys.path.append('backend')
from fastapi.testclient import TestClient
from main import app
import json
from unittest.mock import patch
import language_utils

client = TestClient(app)

message = "आपका अकाउंट बंद कर दिया गया है। अभी सत्यापित करें।" # Hindi

with patch('language_utils.get_translator') as mock_get_translator:
    # Simulate a translation API exception
    mock_translator = mock_get_translator.return_value
    mock_translator.translate.side_effect = Exception("Mocked translation service timeout")
    
    response = client.post("/api/analyze-message", json={"message": message})
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
