# email_verifier.py
import re
import requests
from config import EMAIL_VERIFICATION_API_URL, EMAIL_VERIFICATION_API_KEY

def is_valid_email_syntax(email):
    """Simple regex check for email syntax validity."""
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return True if re.match(regex, email) else False

def verify_email_api(email):
    """Optional: verify email using an API.
    Returns True if email is valid, False otherwise."""
    if not EMAIL_VERIFICATION_API_KEY or EMAIL_VERIFICATION_API_KEY == "YOUR_MAILBOXLAYER_API_KEY":
        print("No valid email verification API key set; skipping API verification.")
        return None

    params = {
        'access_key': EMAIL_VERIFICATION_API_KEY,
        'email': email,
        'smtp': 1,
        'format': 1
    }

    try:
        response = requests.get(EMAIL_VERIFICATION_API_URL, params=params)
        data = response.json()
        # mailboxlayer returns "smtp_check" boolean to indicate if smtp verified mail server
        if data.get("smtp_check") is True:
            return True
        else:
            return False
    except Exception as e:
        print(f"Email verification API call failed: {e}")
        return None
