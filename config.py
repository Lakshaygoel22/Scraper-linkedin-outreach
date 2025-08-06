# config.py

# The URL of the public directory or site to scrape (replace with legal/allowed URL)
TARGET_URL = "https://example-startup-directory.com"

# CSS selectors for scraping - adjust per the website structure
SELECTORS = {
    "company_card": ".company-listing",
    "company_name": ".company-name",
    "company_size": ".company-size",
    "company_website": ".company-website",
    "owner_name": ".owner-name",  # adjust if owner info available
    "owner_email": ".owner-email" # adjust if email info available
}

# Email verification API (optional)
# Example: Use https://mailboxlayer.com/ free tier for syntax/basic validation
EMAIL_VERIFICATION_API_URL = "http://apilayer.net/api/check"
EMAIL_VERIFICATION_API_KEY = "YOUR_MAILBOXLAYER_API_KEY"  # get your free key and use here

# Minimum employees filter (10 to 50)
MIN_EMPLOYEES = 10
MAX_EMPLOYEES = 50
