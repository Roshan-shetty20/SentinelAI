import traceback
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
import os
import re
import joblib
import io
import importlib
import numpy as np

from semantic_analyzer import analyze_semantic_risk
from risk_engine import analyze_scam_patterns
from combined_risk_engine import calculate_combined_risk
from explainable_ai import generate_explanation
from language_utils import process_multilingual
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


TRUSTED_DOMAINS = {
    "s.bflcomm.in",
    "bflcomm.in",
    "bajajfinserv.in",
    "hdfcbank.com",
    "onlinesbi.sbi",
    "icicibank.com"
}

def is_local_url(url):
    import urllib.parse as urlparse
    try:
        parsed = urlparse.urlparse(url)
        hostname = (parsed.hostname or "").lower()
        return hostname in {"localhost", "127.0.0.1", "::1"}
    except Exception:
        return False

def is_trusted_url(url):
    import urllib.parse as urlparse
    try:
        parsed = urlparse.urlparse(url)
        hostname = (parsed.hostname or "").lower()
        if hostname == "": return False
        return hostname in TRUSTED_DOMAINS or any(hostname.endswith("." + td) for td in TRUSTED_DOMAINS)
    except:
        return False

def sanitize_url_for_ml(url):
    import urllib.parse as urlparse
    try:
        parsed = urlparse.urlparse(url)
        # Normalize
        scheme = parsed.scheme.lower()
        hostname = (parsed.hostname or "").lower()
        
        # Remove default ports
        netloc = hostname
        if parsed.port:
            if not ((scheme == 'http' and parsed.port == 80) or (scheme == 'https' and parsed.port == 443)):
                netloc = f"{hostname}:{parsed.port}"
                
        # Strip trailing dot
        if netloc.endswith('.'):
            netloc = netloc[:-1]

        query_params = urlparse.parse_qs(parsed.query, keep_blank_values=True)
        tracking_params = ['_gl', 'gclid', 'fbclid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']
        for param in tracking_params:
            if param in query_params:
                del query_params[param]
        
        new_query = urlparse.urlencode(query_params, doseq=True)
        
        new_url = urlparse.urlunparse((
            scheme,
            netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        return new_url
    except Exception:
        return url

def remove_markdown_links(text):
    import re
    md_pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\s<>"\'\[\]]+|www\.[^\s<>"\'\[\]]+)\)', re.IGNORECASE)
    clean_text = text
    for match in md_pattern.finditer(text):
        anchor = match.group(1).strip()
        clean_text = clean_text.replace(match.group(0), anchor)
    return clean_text


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="SentinelAI",
    description="AI-powered phishing URL and scam message detection API",
    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

import os
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500,https://sentinelai.example.com")
allow_origins_list = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


# ============================================================
# URL MODEL PATHS
# ============================================================

URL_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "url_tfidf_model.pkl"
)

URL_VECTORIZER_PATH = os.path.join(
    MODEL_DIR,
    "url_tfidf_vectorizer.pkl"
)


# ============================================================
# MESSAGE MODEL PATHS
# ============================================================

MESSAGE_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "message_model.pkl"
)

MESSAGE_VECTORIZER_PATH = os.path.join(
    MODEL_DIR,
    "message_vectorizer.pkl"
)


# ============================================================
# MODEL VARIABLES
# ============================================================

url_model = None
url_vectorizer = None
url_model_loaded = False

message_model = None
message_vectorizer = None
message_model_loaded = False

# ============================================================
# SCREENSHOT OCR
# ============================================================

try:
    easyocr = importlib.import_module("easyocr")

    ocr_reader = easyocr.Reader(
        ['en'],
        gpu=False,
        verbose=False
    )

    ocr_loaded = True

    print("EasyOCR loaded successfully")

except Exception as e:
    import traceback as _tb
    _tb.print_exc()

    ocr_reader = None
    ocr_loaded = False

    print(
        "EasyOCR loading error:",
        e
    )

    
# ============================================================
# OCR URL RECOVERY
# ============================================================

# ============================================================
# OCR URL RECOVERY
# ============================================================

def recover_urls_from_ocr(text):

    if not text:
        return []

    normalized = text

    # --------------------------------------------------------
    # 1. Join broken URL pieces across lines
    # Example:
    # usps-redelivery-
    # fees-track
    # ->
    # usps-redelivery-fees-track
    # --------------------------------------------------------

    normalized = re.sub(
        r'(?<=[A-Za-z0-9])-\s*\n\s*(?=[A-Za-z0-9])',
        r'-',
        normalized
    )

    # --------------------------------------------------------
    # 2. Fix OCR mistakes in HTTP / HTTPS (e.g. httpLL)
    # --------------------------------------------------------

    normalized = re.sub(
        r'\b(https?)\s*L+',
        r'\1://',
        normalized,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # 3. Fix OCR "L" after domain extension (e.g. comLpost -> com/post)
    # --------------------------------------------------------

    normalized = re.sub(
        r'\b(com|org|net|in|co|gov|edu)L+',
        r'\1/',
        normalized,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # 4. Fix spaces before domain extensions
    # --------------------------------------------------------

    normalized = re.sub(
        r'([A-Za-z0-9-]+)\s+(com|org|net|in|co|gov|edu)\b',
        r'\1.\2',
        normalized,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # 6. Detect reconstructed URLs
    # --------------------------------------------------------

    url_pattern = (
        r'https?://'
        r'[A-Za-z0-9.-]+'
        r'\.[A-Za-z]{2,}'
        r'(?:/[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=%-]*)?'
    )

    matches = re.findall(
        url_pattern,
        normalized,
        flags=re.IGNORECASE
    )

    recovered_urls = []

    for url in matches:

        url = url.strip()

        url = url.rstrip(
            ".,!?;:"
        )

        if url not in recovered_urls:

            recovered_urls.append(
                url
            )

    print(
        "OCR URL RECOVERY:",
        recovered_urls
    )

    return recovered_urls
# ============================================================
# LOAD URL MODEL
# ============================================================

try:

    url_model = joblib.load(
        URL_MODEL_PATH
    )
    url_model.multi_class = 'ovr'

    url_vectorizer = joblib.load(
        URL_VECTORIZER_PATH
    )

    url_model_loaded = True

    print("URL model loaded successfully")

except Exception as e:

    print(
        "URL model loading error:",
        e
    )


# ============================================================
# LOAD MESSAGE MODEL
# ============================================================

try:

    message_model = joblib.load(
        MESSAGE_MODEL_PATH
    )
    message_model.multi_class = 'ovr'

    message_vectorizer = joblib.load(
        MESSAGE_VECTORIZER_PATH
    )

    message_model_loaded = True

    print(
        "Message model loaded successfully"
    )

except Exception as e:

    print(
        "Message model loading error:",
        e
    )


# ============================================================
# REQUEST MODELS
# ============================================================

class URLRequest(BaseModel):

    url: str


class MessageRequest(BaseModel):

    message: str

class EmailRequest(BaseModel):
    sender: str
    subject: str
    body: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "message":
            "SentinelAI API is running",

        "status":
            "online"

    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {

        "status":
            "healthy",

        "url_model_loaded":
            url_model_loaded,

        "message_model_loaded":
            message_model_loaded,

        "semantic_analyzer":
            True,

        "risk_engine":
            True,

        "fusion_engine":
            True,

        "ocr_engine":
            ocr_loaded

    }


# ============================================================
# URL ANALYZER
# ============================================================

def is_short_url(url):
    import urllib.parse as urlparse
    try:
        parsed = urlparse.urlparse(url)
        if len(url) < 40 and len(parsed.netloc) < 15 and len(parsed.path) < 15:
            return True
        return False
    except:
        return False

def evaluate_url_ml(url):
    import os
    dev_mode = os.environ.get("SENTINELAI_DEV_MODE", "false").lower() == "true"
    
    if dev_mode and is_local_url(url):
        return {
            "prediction_label": "local",
            "raw_prediction": 1,
            "risk_score": 0.0,
            "confidence": 100.0,
            "phishing_probability": 0.0,
            "legitimate_probability": 100.0,
            "reason": "local_development_url"
        }
    
    if is_trusted_url(url):
        return {
            "prediction_label": "legitimate",
            "raw_prediction": 1,
            "risk_score": 0.0,
            "confidence": 100.0,
            "phishing_probability": 0.0,
            "legitimate_probability": 100.0,
            "reason": "trusted_domain"
        }

    sanitized_url = sanitize_url_for_ml(url)
    url_vector = url_vectorizer.transform([sanitized_url])
    probabilities = url_model.predict_proba(url_vector)[0]
    classes = list(url_model.classes_)
    
    phishing_index = classes.index(0)
    legitimate_index = classes.index(1)
    
    phish_prob = float(probabilities[phishing_index])
    legit_prob = float(probabilities[legitimate_index])
    
    PHISHING_THRESHOLD = 0.90
    
    if phish_prob >= PHISHING_THRESHOLD:
        if is_short_url(url) and phish_prob < 0.995:
            prediction_label = "suspicious"
            raw_prediction = 1
            reason = "ml_suspicious_short_url"
            risk_score = 75.0
        else:
            prediction_label = "phishing"
            raw_prediction = 0
            reason = "ml_high_phishing_probability"
            risk_score = phish_prob * 100
    elif legit_prob >= PHISHING_THRESHOLD:
        prediction_label = "legitimate"
        raw_prediction = 1
        reason = "ml_high_legitimate_probability"
        risk_score = phish_prob * 100
    else:
        prediction_label = "suspicious"
        raw_prediction = 1
        reason = "ml_uncertain"
        risk_score = phish_prob * 100
    
    confidence = max(phish_prob, legit_prob) * 100
    
    return {
        "prediction_label": prediction_label,
        "raw_prediction": raw_prediction,
        "risk_score": risk_score,
        "confidence": confidence,
        "phishing_probability": phish_prob * 100,
        "legitimate_probability": legit_prob * 100,
        "reason": reason
    }


@app.post("/api/analyze-url")
def analyze_url(request: URLRequest):
    if not url_model_loaded:
        raise HTTPException(status_code=500, detail="URL machine learning model is not loaded.")
    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")
    try:
        url_eval = evaluate_url_ml(url)
        
        # Combine risk for potential UI integration (even if semantic/pattern is absent)
        combined_result = calculate_combined_risk(url_risk=url_eval["risk_score"])
        
        # Overwrite the prediction if it's suspicious or local to preserve metadata
        prediction_out = url_eval["prediction_label"] if url_eval["prediction_label"] in ["local", "suspicious"] else combined_result["prediction"]
        
        return {
            "url": url,
            "prediction": prediction_out,
            "raw_prediction": url_eval["raw_prediction"],
            "risk_score": combined_result["final_risk_score"],
            "confidence": url_eval["confidence"],
            "risk_level": combined_result["risk_level"],
            "components": combined_result["components"],
            "reasons": [
                url_eval["reason"]
            ],
            "contributing_signals": [
                f"URL Risk: {combined_result['final_risk_score']}"
            ],
            "explainable_ai": {
                "summary": f"The AI Risk Engine classified this URL as {combined_result['risk_level']} risk, contributing to a {prediction_out} verdict.",
                "phishing_probability": url_eval["phishing_probability"],
                "legitimate_probability": url_eval["legitimate_probability"],
                "decision_threshold": 0.90
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print("URL analysis error:", e)
        raise HTTPException(status_code=500, detail="Internal server error occurred during analysis.")


# ============================================================
# MESSAGE SCAM ANALYZER
# ============================================================

@app.post("/api/analyze-message")
def analyze_message(
    request: MessageRequest
):

    # ========================================================
    # CHECK MODEL 1
    # ========================================================

    if not message_model_loaded:

        raise HTTPException(
            status_code=500,
            detail="Message machine learning model is not loaded."
        )

    # ========================================================
    # GET MESSAGE
    # ========================================================

    message = request.message.strip()

    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        processed_message, lang_meta = process_multilingual(message)

        # ====================================================
        # MODEL 1
        # TF-IDF + LOGISTIC REGRESSION
        # ====================================================

        from risk_engine import URL_PATTERN
        
        clean_message = remove_markdown_links(processed_message)
        
        # Remove URLs from text so the natural-language message model doesn't over-penalize them
        text_without_urls = URL_PATTERN.sub(' [URL] ', clean_message).strip()
        
        message_vector = (
            message_vectorizer.transform(
                [text_without_urls]
            )
        )

        raw_prediction = (
            message_model.predict(
                message_vector
            )[0]
        )

        probabilities = (
            message_model.predict_proba(
                message_vector
            )[0]
        )

        classes = list(
            message_model.classes_
        )

        prediction_index = classes.index(
            raw_prediction
        )

        confidence = float(
            probabilities[prediction_index] * 100
        )


        # ----------------------------------------------------
        # MODEL 1 RESULT
        #
        # 0 = safe
        # 1 = scam
        # ----------------------------------------------------

        if int(raw_prediction) == 1:

            model_1_prediction = "scam"

            model_1_risk = confidence

        elif int(raw_prediction) == 0:

            model_1_prediction = "safe"

            model_1_risk = (
                100 - confidence
            )

        else:

            raise HTTPException(
                status_code=500,
                detail=f"Unexpected message prediction: {raw_prediction}"
            )

        # ====================================================
        # MODEL 2
        # SEMANTIC CONTEXT ANALYZER
        # ====================================================

        semantic_result = (
            analyze_semantic_risk(
                clean_message
            )
        )

        model_2_risk = float(
            semantic_result.get(
                "semantic_risk_score",
                0
            )
        )

        # ====================================================
        # MODEL 3
        # SCAM PATTERN / RISK ENGINE
        # ====================================================

        pattern_result = (
            analyze_scam_patterns(
                processed_message
            )
        )

        model_3_risk = float(
            pattern_result.get(
                "pattern_risk_score",
                0
            )
        )

        # ====================================================
        # MODEL 3 ENTITY RESULTS
        # ====================================================

        detected_urls = (
            pattern_result.get(
                "detected_urls",
                []
            )
        )

        detected_phone_numbers = (
            pattern_result.get(
                "detected_phone_numbers",
                []
            )
        )

        detected_emails = (
            pattern_result.get(
                "detected_emails",
                []
            )
        )

        # ====================================================
        # URL ANALYSIS
        # ====================================================

        url_risks = []
        url_results = []

        if detected_urls and url_model_loaded:
            for detected_url in detected_urls:
                try:
                    url_eval = evaluate_url_ml(detected_url)
                    url_risk = url_eval["risk_score"]
                    url_risks.append(url_risk)
                    url_results.append({
                        "url": detected_url,
                        "prediction": url_eval["prediction_label"],
                        "risk_score": round(url_risk, 2),
                        "confidence": round(url_eval["confidence"], 2),
                        "reason": url_eval["reason"]
                    })
                except Exception as url_error:
                    pass
        url_risk = max(url_risks) if url_risks else None


        # ====================================================
        # FUSION ENGINE
        # ====================================================

        credential_signal = any(
            signal.get("type") == "credential_request"
            for signal in pattern_result.get("signals", [])
        )

        combined_result = calculate_combined_risk(
            message_risk=model_1_risk,
            semantic_risk=model_2_risk,
            pattern_risk=model_3_risk,
            url_risk=url_risk,
            credential_signal=credential_signal,
            requires_manual_review=lang_meta.get("requires_manual_review", False)
        )

        final_risk_score = combined_result["final_risk_score"]
        final_prediction = combined_result["prediction"]
        final_confidence = final_risk_score
        
        # ====================================================
# EXPLAINABLE AI
# ====================================================

        xai_result = generate_explanation(
    message=message,
    final_prediction=final_prediction,
    final_risk_score=final_risk_score,

    model_1={
        "prediction": model_1_prediction,
        "risk_score": model_1_risk,
        "confidence": confidence
    },

    model_2=semantic_result,

    model_3=pattern_result,

    detected_urls=detected_urls,
    detected_phone_numbers=detected_phone_numbers,
    detected_emails=detected_emails
)
        xai_result["language_info"] = lang_meta

        
        # RETURN
        # ====================================================

        return {

            "message":
                message,

            "prediction":
                final_prediction,

            "risk_score":
                round(
                    final_risk_score,
                    2
                ),

            "confidence":
                round(
                    final_confidence,
                    2
                ),

            "risk_level":
                combined_result.get("risk_level", "low"),

            "components":
                combined_result.get("components", {}),

            "url_results":
                url_results,

            "reasons":
                xai_result.get("risk_factors", []),

            "contributing_signals": [
                f"{k}: {v['risk_score']}" for k, v in combined_result.get("components", {}).items()
            ],

            "explainable_ai": xai_result,

            "detected_language": lang_meta.get("detected_language", "unknown"),
            "translation_attempted": lang_meta.get("translation_status") in ["success", "failed"],
            "translation_success": lang_meta.get("translation_status") == "success",
            "translated_message": processed_message if lang_meta.get("translation_status") == "success" else None,
            "analysis_source": "translated_text" if lang_meta.get("translation_status") == "success" else "original_text",

            # ------------------------------------------------
            # MODEL 1
            # ------------------------------------------------

            "model_1": {

                "name":
                    "TF-IDF + Logistic Regression",

                "prediction":
                    model_1_prediction,

                "risk_score":
                    round(
                        model_1_risk,
                        2
                    ),

                "confidence":
                    round(
                        confidence,
                        2
                    )

            },

            # ------------------------------------------------
            # MODEL 2
            # ------------------------------------------------

            "model_2": {

                "name":
                    "Semantic Context Analyzer",

                "risk_score":
                    round(
                        model_2_risk,
                        2
                    ),

                "risk_level":
                    semantic_result.get(
                        "risk_level",
                        "unknown"
                    ),

                "social_engineering_detected":
                    semantic_result.get(
                        "social_engineering_detected",
                        False
                    ),

                "signal_count":
                    semantic_result.get(
                        "signal_count",
                        0
                    ),

                "signals":
                    semantic_result.get(
                        "signals",
                        []
                    )

            },

            # ------------------------------------------------
            # MODEL 3
            # ------------------------------------------------

            "model_3": {

                "name":
                    "Scam Pattern / Risk Engine",

                "risk_score":
                    round(
                        model_3_risk,
                        2
                    ),

                "risk_level":
                    pattern_result.get(
                        "risk_level",
                        "unknown"
                    ),

                "signal_count":
                    pattern_result.get(
                        "signal_count",
                        0
                    ),

                "signals":
                    pattern_result.get(
                        "signals",
                        []
                    )

            },

            # ------------------------------------------------
            # DETECTED ENTITIES
            # ------------------------------------------------

            "detected_urls":
                detected_urls,

            "detected_phone_numbers":
                detected_phone_numbers,

            "detected_emails":
                detected_emails

        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            "Message analysis error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred during analysis."
        )

# ============================================================
# EMAIL ANALYZER
# ============================================================

@app.post("/api/analyze-email")
def analyze_email(request: EmailRequest):
    sender = request.sender.strip()
    subject = request.subject.strip()
    body = request.body.strip()
    
    if not sender and not subject and not body:
        raise HTTPException(status_code=400, detail="Email cannot be empty.")
    
    email_text = ""
    if subject:
        email_text += f"Subject: {subject}\n"
    if body:
        email_text += body
        
    msg_req = MessageRequest(message=email_text)
    try:
        res = analyze_message(msg_req)
        # Let's add any email specific fields if needed, but standard response is fine.
        res["sender"] = sender
        res["subject"] = subject
        return res
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error occurred during email analysis.")

@app.post("/api/analyze-screenshot")
async def analyze_screenshot(file: UploadFile = File(...)):
    import io
    import traceback

    # --------------------------------------------------
    # 1. Validate upload
    # --------------------------------------------------
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Empty file uploaded."
        )

    try:
        import numpy as np
        from PIL import Image

        # --------------------------------------------------
        # 2. Validate image
        # --------------------------------------------------
        try:
            check_img = Image.open(io.BytesIO(content))
            check_img.verify()
        except Exception as exc:
            print("IMAGE VALIDATION ERROR:", repr(exc))
            raise HTTPException(
                status_code=415,
                detail="Unsupported or corrupted image file."
            )

        # Re-open after verify()
        img = Image.open(io.BytesIO(content)).convert("RGB")
        img_np = np.array(img)

        # --------------------------------------------------
        # 3. Make sure OCR is available
        # --------------------------------------------------
        global ocr_reader, ocr_loaded

        if not ocr_loaded or ocr_reader is None:
            print("OCR reader is not initialized. Initializing now...")

            try:
                import easyocr

                ocr_reader = easyocr.Reader(
                    ["en"],
                    gpu=False,
                    verbose=False
                )

                ocr_loaded = True

                print("EasyOCR initialized successfully.")

            except Exception as ocr_exc:
                print("=== EASYOCR INITIALIZATION ERROR ===")
                traceback.print_exc()
                print("=== END EASYOCR ERROR ===")

                ocr_loaded = False
                ocr_reader = None

                raise HTTPException(
                    status_code=503,
                    detail="OCR engine could not be initialized. Check the backend terminal for the OCR error."
                )

        # --------------------------------------------------
        # 4. Run OCR
        # --------------------------------------------------
        print("Starting OCR...")

        result = ocr_reader.readtext(img_np)

        print("OCR completed.")
        print("OCR detections:", len(result))

        # --------------------------------------------------
        # 5. Extract text
        # --------------------------------------------------
        extracted_parts = []

        for item in result:
            if len(item) >= 2:
                text = str(item[1]).strip()

                if text:
                    extracted_parts.append(text)

        extracted_text = " ".join(extracted_parts).strip()

        print("Extracted text:", extracted_text[:500])

        # --------------------------------------------------
        # 6. No readable text
        # --------------------------------------------------
        if not extracted_text:
            return {
                "success": True,
                "analyzed": False,
                "prediction": "unknown",
                "risk_score": 0.0,
                "confidence": 0.0,
                "extracted_text": "",
                "filename": file.filename,
                "ocr_confidence": 0.0,
                "reasons": [
                    "No readable text found in screenshot."
                ],
                "components": {},
                "explainable_ai": {},
                "risk_level": "unknown"
            }

        # --------------------------------------------------
        # 7. Use existing message analysis
        # --------------------------------------------------
        msg_req = MessageRequest(
            message=extracted_text
        )

        print("Sending OCR text to message analysis...")

        # analyze_message is a regular synchronous def, NOT async — do NOT await it
        res = analyze_message(msg_req)

        # --------------------------------------------------
        # 8. Convert response to dictionary if necessary
        # --------------------------------------------------
        if not isinstance(res, dict):

            if hasattr(res, "model_dump"):
                res = res.model_dump()

            elif hasattr(res, "dict"):
                res = res.dict()

            else:
                raise TypeError(
                    f"Unexpected analyze_message response type: {type(res)}"
                )

        # --------------------------------------------------
        # 9. Add screenshot metadata
        # --------------------------------------------------
        res["success"] = True
        res["analyzed"] = True
        res["extracted_text"] = extracted_text
        res["filename"] = file.filename

        # --------------------------------------------------
        # 10. Calculate OCR confidence
        # --------------------------------------------------
        confidences = []

        for item in result:
            if len(item) >= 3:
                try:
                    confidences.append(float(item[2]))
                except (TypeError, ValueError):
                    pass

        if confidences:
            avg_conf = (
                sum(confidences) / len(confidences)
            ) * 100
        else:
            avg_conf = 0.0

        res["ocr_confidence"] = round(float(avg_conf), 2)

        print("Screenshot analysis completed successfully.")

        return res

    except HTTPException:
        raise

    except Exception as exc:
        print("=== SCREENSHOT ANALYSIS ERROR ===")
        print("Exception:", repr(exc))
        traceback.print_exc()
        print("=== END SCREENSHOT ANALYSIS ERROR ===")

        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred during screenshot analysis."
        )