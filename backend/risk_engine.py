import re

URL_PATTERN = re.compile(
    "((?:https?://|www\\.)[^\\s<>\"'\\[\\]]+)",
    re.IGNORECASE
)
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
)


# ============================================================
# KEYWORD GROUPS
# ============================================================

PAYMENT_WORDS = [
    "pay",
    "payment",
    "transfer",
    "send money",
    "transaction",
    "fee",
    "charge",
    "deposit",
    "bank transfer",
    "upi",
    "paytm",
    "phonepe",
    "gpay",
    "google pay",
    "credit card",
    "debit card",
    "account number",
    "ifsc"
]


REFUND_WORDS = [
    "refund",
    "cashback",
    "reimbursement",
    "money back",
    "refund approved",
    "refund pending"
]


VERIFICATION_WORDS = [
    "verify",
    "verification",
    "confirm",
    "confirmation",
    "validate",
    "authentication",
    "authenticate"
]


ACCOUNT_WORDS = [
    "account",
    "bank account",
    "profile",
    "login",
    "sign in",
    "security",
    "account security",
    "account activity",
    "unusual activity",
    "suspicious login",
    "new device"
]


CREDENTIAL_WORDS = [
    "password",
    "passcode",
    "otp",
    "one time password",
    "pin",
    "cvv",
    "security code",
    "authentication code",
    "verification code"
]


PERSONAL_INFO_WORDS = [
    "identity",
    "date of birth",
    "dob",
    "address",
    "pan",
    "aadhaar",
    "passport",
    "driving license",
    "social security",
    "personal information",
    "account information",
    "card number"
]


URGENCY_WORDS = [
    "immediately",
    "urgent",
    "urgently",
    "right now",
    "act now",
    "as soon as possible",
    "within 24 hours",
    "within 48 hours",
    "today",
    "deadline",
    "expires",
    "expire",
    "suspended",
    "suspension",
    "blocked",
    "block",
    "restricted",
    "restriction",
    "terminate",
    "terminated",
    "close your account",
    "will be closed"
]


ACTION_WORDS = [
    "click",
    "open",
    "verify",
    "confirm",
    "provide",
    "submit",
    "send",
    "transfer",
    "pay",
    "call",
    "reply",
    "update",
    "download",
    "install"
]


REWARD_WORDS = [
    "winner",
    "won",
    "prize",
    "reward",
    "lottery",
    "jackpot",
    "gift",
    "cash prize",
    "congratulations"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def contains_any(text, words):
    """
    Return matching keywords from a list.
    """

    matches = []

    for word in words:

        if word.lower() in text:

            matches.append(word)

    return matches


def add_signal(
    signals,
    signal_type,
    severity,
    description,
    evidence=None
):
    """
    Add an explainable signal.
    """

    signal = {

        "type": signal_type,

        "severity": severity,

        "description": description

    }

    if evidence:

        signal["evidence"] = evidence

    signals.append(signal)


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_scam_patterns(message):

    text = message.lower().strip()

    signals = []

    risk_score = 0

    # ========================================================
    # ENTITY EXTRACTION
    # ========================================================

    raw_urls = URL_PATTERN.findall(message)
    detected_urls = []
    import re as _re
    for u in raw_urls:
        u = _re.sub(r'[,.)\]]+$', '', u)
        if u not in detected_urls:
            detected_urls.append(u)

    detected_emails = EMAIL_PATTERN.findall(
        message
    )

    detected_phone_numbers = PHONE_PATTERN.findall(
        message
    )

    # ========================================================
    # KEYWORD DETECTION
    # ========================================================

    payment_matches = contains_any(
        text,
        PAYMENT_WORDS
    )

    refund_matches = contains_any(
        text,
        REFUND_WORDS
    )

    verification_matches = contains_any(
        text,
        VERIFICATION_WORDS
    )

    account_matches = contains_any(
        text,
        ACCOUNT_WORDS
    )

    credential_matches = contains_any(
        text,
        CREDENTIAL_WORDS
    )

    personal_matches = contains_any(
        text,
        PERSONAL_INFO_WORDS
    )

    urgency_matches = contains_any(
        text,
        URGENCY_WORDS
    )

    action_matches = contains_any(
        text,
        ACTION_WORDS
    )

    reward_matches = contains_any(
        text,
        REWARD_WORDS
    )

    # ========================================================
    # URL SIGNAL
    # ========================================================

    if detected_urls:

        risk_score += 25

        add_signal(

            signals,

            "suspicious_url",

            "high",

            "Message contains a URL that should be inspected for phishing or malicious activity.",

            detected_urls

        )

    # ========================================================
    # EMAIL SIGNAL
    # ========================================================

    if detected_emails:

        risk_score += 10

        add_signal(

            signals,

            "email_reference",

            "moderate",

            "Message contains an email address.",

            detected_emails

        )

    # ========================================================
    # PHONE SIGNAL
    # ========================================================

    if detected_phone_numbers:

        risk_score += 15

        add_signal(

            signals,

            "phone_number",

            "moderate",

            "Message contains a phone number that may be used for scam contact.",

            detected_phone_numbers

        )

    # ========================================================
    # PAYMENT REQUEST
    # ========================================================

    if payment_matches:

        risk_score += 35

        add_signal(

            signals,

            "payment_request",

            "high",

            "Message contains financial or payment-related language.",

            payment_matches

        )

    # ========================================================
    # REFUND SIGNAL
    # ========================================================

    if refund_matches:

        risk_score += 20

        add_signal(

            signals,

            "refund_reference",

            "moderate",

            "Message references a refund, cashback, or money-back process.",

            refund_matches

        )

    # ========================================================
    # VERIFICATION SIGNAL
    # ========================================================

    if verification_matches:

        risk_score += 15

        add_signal(

            signals,

            "verification_request",

            "high",

            "Message asks the recipient to verify, confirm, or authenticate information.",

            verification_matches

        )

    # ========================================================
    # ACCOUNT SECURITY SIGNAL
    # ========================================================

    if account_matches:

        risk_score += 10

        add_signal(

            signals,

            "account_security",

            "moderate",

            "Message references an account, login, security, or account activity.",

            account_matches

        )

    # ========================================================
    # CREDENTIAL SIGNAL
    # ========================================================

    if credential_matches:

        risk_score += 40

        add_signal(

            signals,

            "credential_request",

            "critical",

            "Message references passwords, OTPs, PINs, CVVs, or authentication credentials.",

            credential_matches

        )

    # ========================================================
    # PERSONAL INFORMATION
    # ========================================================

    if personal_matches:

        risk_score += 20

        add_signal(

            signals,

            "personal_information",

            "high",

            "Message requests or references personal or financial information.",

            personal_matches

        )

    # ========================================================
    # URGENCY / THREAT
    # ========================================================

    if urgency_matches:

        risk_score += 25

        add_signal(

            signals,

            "urgency_pressure",

            "high",

            "Message uses urgency, deadlines, threats, or account restrictions.",

            urgency_matches

        )

    # ========================================================
    # CALL TO ACTION
    # ========================================================

    if action_matches:

        risk_score += 10

        add_signal(

            signals,

            "call_to_action",

            "moderate",

            "Message asks the recipient to perform an action.",

            action_matches

        )

    # ========================================================
    # REWARD / PRIZE
    # ========================================================

    if reward_matches:

        risk_score += 30

        add_signal(

            signals,

            "reward_scam",

            "high",

            "Message contains prize, reward, lottery, or unexpected-winner language.",

            reward_matches

        )

    # ========================================================
    # COMBINATION RULES
    # ========================================================
    #
    # These are more important than individual keywords.
    #
    # ========================================================

    # --------------------------------------------------------
    # ACCOUNT + VERIFICATION
    # --------------------------------------------------------

    if account_matches and verification_matches:

        risk_score += 20

        add_signal(

            signals,

            "account_verification_combination",

            "high",

            "Account/security language is combined with a verification request."

        )

    # --------------------------------------------------------
    # VERIFICATION + PERSONAL INFORMATION
    # --------------------------------------------------------

    if verification_matches and personal_matches:

        risk_score += 20

        add_signal(

            signals,

            "verification_information_combination",

            "high",

            "Verification language is combined with a request for personal information."

        )

    # --------------------------------------------------------
    # VERIFICATION + CREDENTIAL
    # --------------------------------------------------------

    if verification_matches and credential_matches:

        risk_score += 35

        add_signal(

            signals,

            "verification_credential_combination",

            "critical",

            "Verification language is combined with a request for authentication credentials."

        )

    # --------------------------------------------------------
    # PAYMENT + REFUND
    # --------------------------------------------------------

    if payment_matches and refund_matches:

        risk_score += 35

        add_signal(

            signals,

            "refund_payment_combination",

            "critical",

            "A refund-related message also requests payment, transfer, or a fee."

        )

    # --------------------------------------------------------
    # PAYMENT + VERIFICATION
    # --------------------------------------------------------

    if payment_matches and verification_matches:

        risk_score += 30

        add_signal(

            signals,

            "payment_verification_combination",

            "critical",

            "Payment language is combined with a verification or confirmation request."

        )

    # --------------------------------------------------------
    # PAYMENT + URGENCY
    # --------------------------------------------------------

    if payment_matches and urgency_matches:

        risk_score += 30

        add_signal(

            signals,

            "payment_urgency_combination",

            "critical",

            "A payment request is combined with urgency or pressure."

        )

    # --------------------------------------------------------
    # ACCOUNT + URGENCY
    # --------------------------------------------------------

    if account_matches and urgency_matches:

        risk_score += 25

        add_signal(

            signals,

            "account_threat_combination",

            "critical",

            "Account/security language is combined with urgency, restriction, suspension, or threat language."

        )

    # --------------------------------------------------------
    # CREDENTIAL + ACTION
    # --------------------------------------------------------

    if credential_matches and action_matches:

        risk_score += 30

        add_signal(

            signals,

            "credential_action_combination",

            "critical",

            "Authentication credentials are associated with a requested action."

        )

    # ========================================================
    # MULTIPLE HIGH-RISK INDICATORS
    # ========================================================

    high_risk_count = sum(

        1

        for signal in signals

        if signal["severity"]
        in ["high", "critical"]

    )

    if high_risk_count >= 3:

        risk_score += 25

        add_signal(

            signals,

            "multiple_risk_indicators",

            "critical",

            "Multiple high-risk scam indicators appear together."

        )

    # ========================================================
    # CAP SCORE
    # ========================================================

    risk_score = min(
        risk_score,
        100
    )

    # ========================================================
    # RISK LEVEL
    # ========================================================

    if risk_score >= 70:

        risk_level = "high"

    elif risk_score >= 40:

        risk_level = "medium"

    elif risk_score >= 20:

        risk_level = "low"

    else:

        risk_level = "minimal"

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "pattern_risk_score":
            round(
                risk_score,
                2
            ),

        "risk_level":
            risk_level,

        "signal_count":
            len(signals),

        "signals":
            signals,

        "detected_urls":
            detected_urls,

        "detected_phone_numbers":
            detected_phone_numbers,

        "detected_emails":
            detected_emails

    }