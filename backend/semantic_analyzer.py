import re


# ============================================================
# SENTINELAI — ADVANCED SEMANTIC / CONTEXT ANALYZER
# ============================================================


def analyze_semantic_risk(message: str):

    text = message.lower().strip()

    signals = []
    score = 0

    # ========================================================
    # HELPER FUNCTION
    # ========================================================

    def add_signal(signal_type, risk, points, reason):

        nonlocal score

        signals.append({
            "type": signal_type,
            "risk": risk,
            "score": points,
            "reason": reason
        })

        score += points

    # ========================================================
    # 1. ACCOUNT / SECURITY
    # ========================================================

    account_patterns = [
        r"\baccount\b",
        r"\blogin\b",
        r"\bsign.?in\b",
        r"\bsecurity alert\b",
        r"\bsuspicious activity\b",
        r"\bunusual activity\b",
        r"\baccount activity\b",
        r"\baccount access\b",
        r"\bsecurity\b"
    ]

    has_account_security = any(
        re.search(pattern, text)
        for pattern in account_patterns
    )

    if has_account_security:

        add_signal(
            "account_security",
            "moderate",
            10,
            "Message references an account or security-related activity."
        )

    # ========================================================
    # 2. VERIFICATION
    # ========================================================

    verification_patterns = [
        r"\bverify\b",
        r"\bverification\b",
        r"\bconfirm\b",
        r"\bconfirmation\b",
        r"\bvalidate\b",
        r"\bverify your identity\b",
        r"\bconfirm your identity\b",
        r"\bupdate your information\b",
        r"\bcomplete verification\b"
    ]

    has_verification = any(
        re.search(pattern, text)
        for pattern in verification_patterns
    )

    if has_verification:

        add_signal(
            "verification_request",
            "high",
            20,
            "Message asks the recipient to verify or confirm information."
        )

    # ========================================================
    # 3. CREDENTIALS / OTP
    # ========================================================

    credential_patterns = [
        r"\bpassword\b",
        r"\bpin\b",
        r"\botp\b",
        r"\bone.?time password\b",
        r"\bpasscode\b",
        r"\bsecurity code\b",
        r"\bcredentials\b",
        r"\blogin details\b"
    ]

    has_credentials = any(
        re.search(pattern, text)
        for pattern in credential_patterns
    )

    if has_credentials:

        add_signal(
            "credential_request",
            "critical",
            35,
            "Message references passwords, OTPs, PINs, or authentication credentials."
        )

    # ========================================================
    # 4. PERSONAL INFORMATION
    # ========================================================

    personal_patterns = [
        r"\bpersonal information\b",
        r"\bpersonal details\b",
        r"\bdate of birth\b",
        r"\bidentity\b",
        r"\bidentification\b",
        r"\bpan\b",
        r"\baadhaar\b",
        r"\bsocial security\b",
        r"\bcard number\b",
        r"\bbank details\b",
        r"\bbanking information\b"
    ]

    has_personal_info = any(
        re.search(pattern, text)
        for pattern in personal_patterns
    )

    if has_personal_info:

        add_signal(
            "personal_information",
            "high",
            20,
            "Message references sensitive personal or financial information."
        )

    # ========================================================
    # 5. PAYMENT / MONEY
    # ========================================================

    payment_patterns = [
        r"\bpayment\b",
        r"\bpay now\b",
        r"\btransfer\b",
        r"\btransaction\b",
        r"\brefund\b",
        r"\bdeposit\b",
        r"\bfee\b",
        r"\bupi\b",
        r"\bbank transfer\b",
        r"\bcredit card\b",
        r"\bdebit card\b",
        r"\bsend money\b",
        r"\bsend payment\b"
    ]

    has_payment = any(
        re.search(pattern, text)
        for pattern in payment_patterns
    )

    if has_payment:

        add_signal(
            "financial_activity",
            "high",
            20,
            "Message contains financial or payment-related language."
        )

    # ========================================================
    # 6. PRIZE / REWARD SCAM
    # ========================================================

    reward_patterns = [
        r"\bwon\b",
        r"\bwinner\b",
        r"\bcongratulations\b",
        r"\bprize\b",
        r"\breward\b",
        r"\blottery\b",
        r"\bjackpot\b",
        r"\bgift card\b",
        r"\bfree gift\b",
        r"\bcash prize\b",
        r"\bclaim your\b"
    ]

    has_reward = any(
        re.search(pattern, text)
        for pattern in reward_patterns
    )

    if has_reward:

        add_signal(
            "reward_scam",
            "high",
            25,
            "Message contains prize, reward, lottery, or unexpected-winner language."
        )

    # ========================================================
    # 7. URGENCY
    # ========================================================

    urgency_patterns = [
        r"\burgent\b",
        r"\bimmediately\b",
        r"\bimmediate action\b",
        r"\bact now\b",
        r"\bwithin \d+ (minutes?|hours?)\b",
        r"\bexpires?\b",
        r"\blast chance\b",
        r"\bdeadline\b",
        r"\bas soon as possible\b",
        r"\bwithout delay\b",
        r"\bavoid suspension\b",
        r"\bdo this now\b"
    ]

    has_urgency = any(
        re.search(pattern, text)
        for pattern in urgency_patterns
    )

    if has_urgency:

        add_signal(
            "urgency_pressure",
            "high",
            15,
            "Message uses urgency or time pressure to influence the recipient."
        )

    # ========================================================
    # 8. THREAT / CONSEQUENCE
    # ========================================================

    threat_patterns = [
        r"\bwill be blocked\b",
        r"\bwill be suspended\b",
        r"\bwill be closed\b",
        r"\baccount blocked\b",
        r"\baccount suspended\b",
        r"\blegal action\b",
        r"\bpenalty\b",
        r"\bfine\b",
        r"\bdeactivated\b",
        r"\bterminated\b",
        r"\blimited access\b"
    ]

    has_threat = any(
        re.search(pattern, text)
        for pattern in threat_patterns
    )

    if has_threat:

        add_signal(
            "threat_or_consequence",
            "high",
            20,
            "Message threatens account loss, penalties, suspension, or other consequences."
        )

    # ========================================================
    # 9. TRUST / REASSURANCE
    # ========================================================

    reassurance_patterns = [
        r"\bfor your security\b",
        r"\bfor your safety\b",
        r"\bthis is not a scam\b",
        r"\bdo not worry\b",
        r"\bsafely\b",
        r"\btrusted\b",
        r"\bprotect your account\b",
        r"\bkeep your account safe\b"
    ]

    has_reassurance = any(
        re.search(pattern, text)
        for pattern in reassurance_patterns
    )

    if has_reassurance:

        add_signal(
            "trust_building",
            "low",
            3,
            "Message uses reassurance or safety language."
        )

    # ========================================================
    # 10. CALL TO ACTION
    # ========================================================

    action_patterns = [
        r"\bclick\b",
        r"\btap\b",
        r"\bvisit\b",
        r"\bopen\b",
        r"\bgo to\b",
        r"\breply\b",
        r"\bcall us\b",
        r"\bcontact us\b",
        r"\bdownload\b",
        r"\bcomplete\b",
        r"\bsubmit\b",
        r"\bclaim\b",
        r"\bactivate\b"
    ]

    has_action = any(
        re.search(pattern, text)
        for pattern in action_patterns
    )

    if has_action:

        add_signal(
            "call_to_action",
            "moderate",
            10,
            "Message asks the recipient to perform an action."
        )

    # ========================================================
    # 11. URL
    # ========================================================

    urls = re.findall(
        r"(https?://[^\s]+|www\.[^\s]+)",
        text
    )

    has_url = len(urls) > 0

    if has_url:

        add_signal(
            "url_present",
            "moderate",
            15,
            "Message contains a URL."
        )

    # ========================================================
    # 12. PHONE NUMBER
    # ========================================================

    phone_numbers = re.findall(
        r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b",
        text
    )

    if phone_numbers:

        add_signal(
            "phone_number",
            "low",
            5,
            "Message contains a phone number."
        )

    # ========================================================
    # 13. EMAIL
    # ========================================================

    emails = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    if emails:

        add_signal(
            "email_present",
            "low",
            5,
            "Message contains an email address."
        )

    # ========================================================
    # 14. DELIVERY / PACKAGE SCAM
    # ========================================================

    delivery_patterns = [
        r"\bpackage\b",
        r"\bparcel\b",
        r"\bdelivery\b",
        r"\bcourier\b",
        r"\bshipment\b",
        r"\btracking\b",
        r"\bdelivery failed\b",
        r"\bdelivery attempt\b"
    ]

    has_delivery = any(
        re.search(pattern, text)
        for pattern in delivery_patterns
    )

    if has_delivery:

        add_signal(
            "delivery_scam_pattern",
            "moderate",
            15,
            "Message contains delivery, courier, parcel, or shipment language."
        )

    # ========================================================
    # 15. JOB / RECRUITMENT SCAM
    # ========================================================

    job_patterns = [
        r"\bjob offer\b",
        r"\bwork from home\b",
        r"\bpart.?time job\b",
        r"\brecruitment\b",
        r"\bhiring\b",
        r"\bselected for the position\b",
        r"\bearn \₹?\s?\d+",
        r"\bsalary\b"
    ]

    has_job = any(
        re.search(pattern, text)
        for pattern in job_patterns
    )

    if has_job:

        add_signal(
            "job_scam_pattern",
            "moderate",
            15,
            "Message contains recruitment, employment, or earning-related language."
        )

    # ========================================================
    # 16. KYC / BANKING
    # ========================================================

    kyc_patterns = [
        r"\bkyc\b",
        r"\bkyc update\b",
        r"\bkyc verification\b",
        r"\bbank account\b",
        r"\bnet banking\b",
        r"\bupi\b",
        r"\bcredit card\b",
        r"\bdebit card\b"
    ]

    has_kyc = any(
        re.search(pattern, text)
        for pattern in kyc_patterns
    )

    if has_kyc:

        add_signal(
            "banking_kyc_pattern",
            "high",
            20,
            "Message references banking, KYC, cards, or payment services."
        )

    # ========================================================
    # 17. SOCIAL ENGINEERING COMBINATIONS
    # ========================================================

    social_engineering = False

    # Account + verification
    if has_account_security and has_verification:
        social_engineering = True

    # Verification + action
    if has_verification and has_action:
        social_engineering = True

    # Urgency + action
    if has_urgency and has_action:
        social_engineering = True

    # Threat + action
    if has_threat and has_action:
        social_engineering = True

    # Reward + action
    if has_reward and has_action:
        social_engineering = True

    # Credential + urgency
    if has_credentials and has_urgency:
        social_engineering = True

    if social_engineering:

        add_signal(
            "social_engineering",
            "high",
            15,
            "Multiple behavioral signals indicate possible social-engineering tactics."
        )

    # ========================================================
    # 18. HIGH-RISK COMBINATIONS
    # ========================================================

    # Credential phishing
    if has_credentials and has_action:

        add_signal(
            "credential_phishing",
            "critical",
            20,
            "Authentication information is combined with a requested action."
        )

    # Financial manipulation
    if has_payment and has_urgency:

        add_signal(
            "financial_pressure",
            "critical",
            20,
            "Financial activity is combined with urgency or pressure."
        )

    # Reward manipulation
    if has_reward and has_url:

        add_signal(
            "reward_link",
            "high",
            20,
            "Reward or prize language is combined with a URL."
        )

    # ========================================================
    # CAP SCORE
    # ========================================================

    score = min(score, 100)

    # ========================================================
    # RISK LEVEL
    # ========================================================

    if score >= 70:

        risk_level = "high"

    elif score >= 40:

        risk_level = "medium"

    elif score >= 20:

        risk_level = "low"

    else:

        risk_level = "minimal"

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "semantic_risk_score": round(score, 2),

        "risk_level": risk_level,

        "signals": signals,

        "signal_count": len(signals),

        "social_engineering_detected": social_engineering,

        "detected_urls": urls,

        "detected_phone_numbers": phone_numbers,

        "detected_emails": emails
    }