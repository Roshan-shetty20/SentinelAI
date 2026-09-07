from semantic_analyzer import analyze_semantic_risk


# ============================================================
# TEST MESSAGES
# ============================================================

messages = [

    # Safe
    "Hello, your account is secure. Thank you for using our service.",

    # Sophisticated phishing
    "Your account has unusual activity. Please verify your identity immediately to avoid suspension.",

    # Prize scam
    "Congratulations! You won a prize. Click the link to claim your reward.",

    # Social engineering
    "For your security, please confirm your account information.",

    # Credential scam
    "Your security verification is required. Please provide your OTP and password."
]


# ============================================================
# RUN TESTS
# ============================================================

for number, message in enumerate(messages, start=1):

    print("\n")
    print("=" * 70)
    print(f"TEST {number}")
    print("=" * 70)

    print("\nMESSAGE:")
    print(message)

    result = analyze_semantic_risk(message)

    print("\nSEMANTIC RISK SCORE:")
    print(result["semantic_risk_score"])

    print("\nRISK LEVEL:")
    print(result["risk_level"])

    print("\nSOCIAL ENGINEERING:")
    print(result["social_engineering_detected"])

    print("\nSIGNALS:")

    for signal in result["signals"]:

        print(
            f"  [{signal['risk'].upper()}] "
            f"{signal['type']} → "
            f"{signal['reason']}"
        )