import re


# ============================================================
# SENTINELAI — EXPLAINABLE AI
# ============================================================
#
# Converts the outputs of Model 1, Model 2 and Model 3
# into a human-readable explanation.
#
# ============================================================


def generate_explanation(
    message,
    final_prediction,
    final_risk_score,
    model_1,
    model_2,
    model_3,
    detected_urls=None,
    detected_phone_numbers=None,
    detected_emails=None
):

    detected_urls = detected_urls or []
    detected_phone_numbers = detected_phone_numbers or []
    detected_emails = detected_emails or []

    explanations = []
    risk_factors = []
    positive_signals = []

    message_lower = message.lower()


    # ========================================================
    # MODEL 1 EXPLANATION
    # ========================================================

    model_1_prediction = model_1.get("prediction", "unknown")
    model_1_risk = float(model_1.get("risk_score", 0))

    if model_1_prediction == "scam":

        explanations.append(
            "The machine-learning classifier detected patterns "
            "similar to previously identified scam or spam messages."
        )

        risk_factors.append(
            "ML classifier detected scam-like language"
        )

    elif model_1_prediction == "safe" and model_1_risk < 30:

        positive_signals.append(
            "The message has low similarity to known spam patterns."
        )

    elif model_1_prediction == "safe":

        explanations.append(
            "The traditional ML classifier did not strongly "
            "identify the message as spam."
        )


    # ========================================================
    # MODEL 2 — SEMANTIC SIGNALS
    # ========================================================

    semantic_signals = model_2.get("signals", [])

    for signal in semantic_signals:

        signal_type = signal.get("type", "")
        risk = signal.get("risk", "")
        reason = signal.get("reason", "")

        if signal_type == "social_engineering":
            continue

        if signal_type == "account_security":

            risk_factors.append(
                "Account or security-related language detected"
            )

        elif signal_type == "verification_request":

            risk_factors.append(
                "The message asks the recipient to verify or confirm information"
            )

        elif signal_type == "credential_request":

            risk_factors.append(
                "The message references sensitive authentication credentials such as OTPs or passwords"
            )

        elif signal_type == "personal_information":

            risk_factors.append(
                "The message requests or references personal information"
            )

        elif signal_type == "urgency_pressure":

            risk_factors.append(
                "Urgency or pressure is used to influence the recipient"
            )

        elif signal_type == "financial_activity":

            risk_factors.append(
                "Financial or payment-related activity is requested"
            )

        elif signal_type == "call_to_action":

            risk_factors.append(
                "The recipient is instructed to perform an action"
            )

        elif signal_type == "trust_building":

            risk_factors.append(
                "Reassuring or trust-building language is used"
            )

        elif signal_type == "reward_scam":

            risk_factors.append(
                "Unexpected prize, reward or winning language detected"
            )

        elif reason:

            risk_factors.append(reason)


    # ========================================================
    # MODEL 3 — PATTERN SIGNALS
    # ========================================================

    pattern_signals = model_3.get("signals", [])

    for signal in pattern_signals:

        signal_type = signal.get("type", "")
        severity = signal.get("severity", "")
        description = signal.get("description", "")

        if signal_type in [
            "multiple_risk_indicators",
            "credential_action_combination"
        ]:
            continue

        if signal_type == "payment_request":

            risk_factors.append(
                "The message requests or references a payment or money transfer"
            )

        elif signal_type == "refund_reference":

            risk_factors.append(
                "The message uses refund or cashback language"
            )

        elif signal_type == "verification_request":

            risk_factors.append(
                "Verification or confirmation is requested"
            )

        elif signal_type == "credential_request":

            risk_factors.append(
                "Authentication credentials such as OTP or password are referenced"
            )

        elif signal_type == "personal_information":

            risk_factors.append(
                "Personal or financial information is involved"
            )

        elif signal_type == "account_security":

            risk_factors.append(
                "Account or security activity is referenced"
            )

        elif signal_type == "urgency_pressure":

            risk_factors.append(
                "The message creates urgency or pressure"
            )

        elif signal_type == "call_to_action":

            risk_factors.append(
                "The recipient is instructed to take an action"
            )

        elif signal_type == "account_verification_combination":

            risk_factors.append(
                "Account/security language is combined with a verification request"
            )

        elif signal_type == "verification_information_combination":

            risk_factors.append(
                "Verification is combined with a request for personal information"
            )

        elif signal_type == "refund_payment_combination":

            risk_factors.append(
                "A refund-related message also requests payment or a fee"
            )

        elif signal_type == "payment_verification_combination":

            risk_factors.append(
                "Payment language is combined with verification activity"
            )

        elif description:

            risk_factors.append(description)


    # ========================================================
    # URL / PHONE / EMAIL EVIDENCE
    # ========================================================

    if detected_urls:

        risk_factors.append(
            f"The message contains {len(detected_urls)} URL(s), "
            "which may require additional verification."
        )

    if detected_phone_numbers:

        risk_factors.append(
            f"The message contains {len(detected_phone_numbers)} phone number(s)."
        )

    if detected_emails:

        risk_factors.append(
            f"The message contains {len(detected_emails)} email address(es)."
        )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    risk_factors = list(dict.fromkeys(risk_factors))
    positive_signals = list(dict.fromkeys(positive_signals))


    # ========================================================
    # SOCIAL ENGINEERING
    # ========================================================

    social_engineering = model_2.get(
        "social_engineering_detected",
        False
    )

    if social_engineering:

        explanations.append(
            "Multiple behavioral indicators suggest possible "
            "social-engineering tactics."
        )


    # ========================================================
    # FINAL INTERPRETATION
    # ========================================================

    if final_risk_score >= 80:

        verdict_explanation = (
            "High-risk indicators strongly suggest that this "
            "message may be a scam or malicious social-engineering attempt."
        )

    elif final_risk_score >= 60:

        verdict_explanation = (
            "Several suspicious indicators were detected. "
            "The message should be treated with caution."
        )

    elif final_risk_score >= 35:

        verdict_explanation = (
            "The message contains some suspicious characteristics, "
            "but the available evidence is not sufficient to classify "
            "it as a high-confidence scam."
        )

    else:

        verdict_explanation = (
            "No significant scam indicators were detected."
        )


    # ========================================================
    # SPECIAL HIGH-RISK COMBINATIONS
    # ========================================================

    if (
        "credential_request" in [
            s.get("type")
            for s in semantic_signals
        ]
    ):

        explanations.append(
            "Requesting OTPs, passwords, PINs or similar credentials "
            "is a major security warning sign."
        )


    if (
        "payment_request" in [
            s.get("type")
            for s in pattern_signals
        ]
        and
        "refund_payment_combination" in [
            s.get("type")
            for s in pattern_signals
        ]
    ):

        explanations.append(
            "Legitimate refunds generally should not require "
            "the recipient to send a separate verification fee."
        )


    # ========================================================
    # SAFE MESSAGE EXPLANATION
    # ========================================================

    if final_risk_score < 20:

        if not risk_factors:

            explanations.append(
                "The message does not contain significant "
                "payment, credential, verification, urgency, "
                "or social-engineering indicators."
            )


    # ========================================================
    # MAIN EXPLANATION
    # ========================================================

    if final_prediction == "scam":

        summary = (
            "SentinelAI classified this message as a potential scam "
            "because multiple independent detection layers identified "
            "risk indicators."
        )

    elif final_prediction == "suspicious":

        summary = (
            "SentinelAI classified this message as suspicious because "
            "some behavioral or contextual indicators were detected."
        )

    else:

        summary = (
            "SentinelAI currently considers this message relatively safe "
            "based on the available evidence."
        )


    # ========================================================
    # RETURN XAI RESULT
    # ========================================================

    return {

        "summary": summary,

        "verdict_explanation": verdict_explanation,

        "risk_factors": risk_factors,

        "positive_signals": positive_signals,

        "social_engineering_detected": social_engineering,

        "models_used": [
            "TF-IDF + Logistic Regression",
            "Semantic Context Analyzer",
            "Scam Pattern / Risk Engine",
            "Risk Fusion Engine"
        ],

        "explanation_count": len(risk_factors)

    }