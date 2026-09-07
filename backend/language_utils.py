import re
import os
import logging
import joblib
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

try:
    from langdetect import detect, detect_langs
    from langdetect.lang_detect_exception import LangDetectException
except ImportError:
    detect = None

try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

from risk_engine import URL_PATTERN, EMAIL_PATTERN, PHONE_PATTERN

logger = logging.getLogger(__name__)

try:
    _message_vectorizer = joblib.load('backend/models/message_vectorizer.pkl')
    _english_vocab = _message_vectorizer.vocabulary_
except Exception as e:
    logger.warning(f"Failed to load vectorizer for language utils: {e}")
    _english_vocab = {}

# Basic in-memory cache to save API calls
_translation_cache = {}


class TranslationProvider:
    def translate(self, text: str) -> str:
        raise NotImplementedError("Subclasses must implement translate()")

class EnvTranslationProvider(TranslationProvider):
    def __init__(self):
        self.api_key = os.environ.get("TRANSLATION_API_KEY")
        
    def translate(self, text: str) -> str:
        if not self.api_key:
            raise ValueError("TRANSLATION_API_KEY not configured.")
        raise NotImplementedError("Official API integration not implemented.")

class FallbackTranslationProvider(TranslationProvider):
    def translate(self, text: str) -> str:
        if GoogleTranslator is None:
            raise ValueError("deep-translator not installed.")
        return GoogleTranslator(source='auto', target='en').translate(text)

def get_translator() -> TranslationProvider:
    if os.environ.get("TRANSLATION_API_KEY"):
        return EnvTranslationProvider()
    return FallbackTranslationProvider()


def detect_language_composition(text: str) -> dict:
    meta = {
        "detected_language": "en",
        "confidence": 1.0,
        "language_mode": "english",
        "translation_status": "not_required",
        "analysis_status": "success",
        "requires_manual_review": False,
        "error": None
    }
    
    if not text.strip():
        return meta

    try:
        langs = {l.lang: l.prob for l in detect_langs(text)}
        best_lang = max(langs.keys(), key=lambda k: langs[k])
        meta["detected_language"] = best_lang
        meta["confidence"] = langs[best_lang]
    except Exception:
        langs = {'en': 1.0}
        meta["detected_language"] = "en"
        meta["confidence"] = 1.0

    en_prob = langs.get('en', 0.0)

    import re as regex
    words = [w.lower() for w in regex.findall(r'\b[a-zA-Z]+\b', text) if len(w) > 1]
    
    if not words:
        meta["language_mode"] = "english" if en_prob > 0.5 else "non_english"
    else:
        recognized = [w for w in words if w in _english_vocab or w in ENGLISH_STOP_WORDS]
        ratio = len(recognized) / len(words)
        
        if en_prob < 0.3:
            meta["language_mode"] = "non_english"
        elif ratio < 0.75 and len(words) >= 4:
            meta["language_mode"] = "mixed"
        else:
            meta["language_mode"] = "english"
            
    return meta

def protect_sensitive_tokens(text: str):
    mapping = {}
    
    url_matches = list(URL_PATTERN.finditer(text))
    for i, match in enumerate(reversed(url_matches)):
        placeholder = f"__URL_{i}__"
        original = match.group(0)
        mapping[placeholder.strip()] = original
        start, end = match.span()
        text = text[:start] + placeholder + text[end:]
        
    email_matches = list(EMAIL_PATTERN.finditer(text))
    for i, match in enumerate(reversed(email_matches)):
        placeholder = f"__EMAIL_{i}__"
        original = match.group(0)
        mapping[placeholder.strip()] = original
        start, end = match.span()
        text = text[:start] + placeholder + text[end:]
        
    phone_matches = list(PHONE_PATTERN.finditer(text))
    for i, match in enumerate(reversed(phone_matches)):
        placeholder = f"__PHONE_{i}__"
        original = match.group(0)
        mapping[placeholder.strip()] = original
        start, end = match.span()
        text = text[:start] + placeholder + text[end:]
        
    return text, mapping

def restore_sensitive_tokens(text: str, mapping: dict) -> str:
    for placeholder, original in mapping.items():
        text = text.replace(placeholder, original)
        text = text.replace(placeholder.lower(), original)
        # Deep translator sometimes adds spaces around brackets
        text = text.replace(placeholder.strip(), original)
    return text

def translate_to_english(text: str) -> str:
    text = text.strip()
    if not text:
        return text
        
    if text in _translation_cache:
        return _translation_cache[text]
        
    try:
        translator = get_translator()
        translated = translator.translate(text)
        
        ERROR_SIGNATURES = [
            "error 500", "server error", "internal server error",
            "bad request", "unauthorized", "too many requests",
            "service unavailable"
        ]
        lower_trans = translated.lower()
        for sig in ERROR_SIGNATURES:
            if sig in lower_trans:
                raise ValueError(f"Provider returned error string: {translated}")
        
        if len(_translation_cache) > 1000:
            _translation_cache.pop(next(iter(_translation_cache)))
            
        _translation_cache[text] = translated
        return translated
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise

def process_multilingual(text: str) -> tuple:
    meta = {
        "detected_language": "en",
        "confidence": 1.0,
        "translation_status": "not_required",
        "analysis_status": "success",
        "requires_manual_review": False,
        "error": None
    }
    
    if not text.strip():
        return text, meta
        
    protected_text, mapping = protect_sensitive_tokens(text)
    
    detect_text = protected_text
    for placeholder in mapping.keys():
        detect_text = detect_text.replace(placeholder, "")
        
    comp_meta = detect_language_composition(detect_text)
    meta.update(comp_meta)
    
    if meta["language_mode"] in ["non_english", "mixed"]:
        try:
            translated_text = translate_to_english(protected_text)
            if translated_text.strip():
                if translated_text == protected_text and meta["language_mode"] == "non_english":
                    raise ValueError("Translation returned original or empty text.")
                meta["translation_status"] = "success"
                final_text = restore_sensitive_tokens(translated_text, mapping)
                return final_text, meta
            else:
                raise ValueError("Translation returned original or empty text.")
        except Exception as e:
            meta["translation_status"] = "failed"
            meta["analysis_status"] = "translation_failed"
            meta["requires_manual_review"] = True
            meta["error"] = str(e)
            
    final_text = restore_sensitive_tokens(protected_text, mapping)
    return final_text, meta
