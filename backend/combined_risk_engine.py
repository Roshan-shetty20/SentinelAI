# ============================================================
# SENTINELAI — COMBINED RISK ENGINE
# ============================================================

def calculate_combined_risk(
    message_risk=None,
    semantic_risk=None,
    pattern_risk=None,
    url_risk=None,
    sender_risk=None,
    credential_signal=False,
    requires_manual_review=False
):
    """
    Central risk fusion engine for SentinelAI.

    Only available signals are included in the weighted score.
    Missing signals are NOT treated as zero-risk evidence.
    """

    # ========================================================
    # NORMALIZE INPUTS
    # ========================================================

    signals = {}

    if message_risk is not None:
        signals["message_risk"] = float(message_risk)

    if semantic_risk is not None:
        signals["semantic_risk"] = float(semantic_risk)

    if pattern_risk is not None:
        signals["pattern_risk"] = float(pattern_risk)

    if url_risk is not None:
        signals["url_risk"] = float(url_risk)

    if sender_risk is not None:
        signals["sender_risk"] = float(sender_risk)

    # Keep scores between 0 and 100
    signals = {
        key: max(0.0, min(value, 100.0))
        for key, value in signals.items()
    }

    # ========================================================
    # BASE WEIGHTS
    # ========================================================

    weights = {
        "message_risk": 0.30,
        "semantic_risk": 0.20,
        "pattern_risk": 0.15,
        "url_risk": 0.35,
        "sender_risk": 0.05
    }

    # ========================================================
    # DYNAMIC WEIGHT NORMALIZATION
    # ========================================================

    # Only available signals participate in scoring.
    available_weight = sum(
        weights[key]
        for key in signals
    )

    if available_weight == 0:
        final_risk_score = 0.0
    else:
        final_risk_score = sum(
            signals[key] *
            (weights[key] / available_weight)
            for key in signals
        )

    # ========================================================
    # HIGH-RISK URL OVERRIDE (CONTEXTUAL)
    # ========================================================

    if url_risk is not None and url_risk >= 80:
        if message_risk is not None and message_risk < 20:
            # If the URL is highly suspicious but the message NLP is extremely safe,
            # we cap the override to SUSPICIOUS (75) to prevent blind false-positives
            # on legitimate short-URLs that the URL model flags purely lexically.
            final_risk_score = max(
                final_risk_score,
                75
            )
        else:
            final_risk_score = max(
                final_risk_score,
                80
            )

    # ========================================================
    # HIGH-RISK SEMANTIC + PATTERN OVERRIDE
    # ========================================================

    if (
        semantic_risk is not None
        and pattern_risk is not None
        and semantic_risk >= 70
        and pattern_risk >= 70
    ):
        final_risk_score = max(
            final_risk_score,
            75
        )


    # ========================================================
    # CAP SCORE
    # ========================================================

    final_risk_score = max(
        0,
        min(
            final_risk_score,
            100
        )
    )

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    if requires_manual_review:
        prediction = "review"
    elif final_risk_score >= 70:
        prediction = "scam"
    elif final_risk_score >= 40:
        prediction = "suspicious"
    else:
        prediction = "safe"

    # ========================================================
    # RISK LEVEL
    # ========================================================

    if final_risk_score >= 70:
        risk_level = "high"

    elif final_risk_score >= 40:
        risk_level = "medium"

    else:
        risk_level = "low"

    # ========================================================
    # COMPONENT BREAKDOWN
    # ========================================================

    component_breakdown = {}

    for key, value in signals.items():
        normalized_weight = (
            weights[key] / available_weight
            if available_weight > 0
            else 0
        )

        component_breakdown[key] = {
            "risk_score": round(value, 2),
            "weight": round(
                normalized_weight * 100,
                2
            ),
            "contribution": round(
                value * normalized_weight,
                2
            )
        }

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "final_risk_score": round(
            final_risk_score,
            2
        ),

        "prediction": prediction,

        "risk_level": risk_level,

        "components": component_breakdown,

        "credential_override": credential_signal,

        "high_risk_url_override": (
            url_risk is not None
            and url_risk >= 80
        ),

        "semantic_pattern_override": (
            semantic_risk is not None
            and pattern_risk is not None
            and semantic_risk >= 70
            and pattern_risk >= 70
        )
    }