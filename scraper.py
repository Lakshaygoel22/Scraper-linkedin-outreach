# scraper.py

import requests
from bs4 import BeautifulSoup
import csv
import time
from config import TARGET_URL, SELECTORS, MIN_EMPLOYEES, MAX_EMPLOYEES
from email_verifier import is_valid_email_syntax, verify_email_api

HEADERS = {
    "User-Agent": "Mozilla/5.0 (LeadScraperBot/1.0)"
}

def parse_employee_range(size_text):
    """Parse employee size text to extract minimal and maximal employee numbers.
    Example: 'Company size: 10-50 employees' -> (10, 50)
    Should be adjusted based on actual website format."""
    import re
    match = re.search(r'(\d+)\s*-\s*(\d+)', size_text)
    if match:
        min_emp = int(match.group(1))
        max_emp = int(match.group(2))
        return min_emp, max_emp
    else:
        # Unable to parse range, fallback
        return None, None

def scrape():
    response = requests.get(TARGET_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to access {TARGET_URL} with status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    entries = []
    company_cards = soup.select(SELECTORS["company_card"])
    print(f"Found {len(company_cards)} companies on page.")

    for card in company_cards:
        try:
            name_tag = card.select_one(SELECTORS["company_name"])
            size_tag = card.select_one(SELECTORS["company_size"])
            website_tag = card.select_one(SELECTORS["company_website"])
            owner_name_tag = card.select_one(SELECTORS.get("owner_name", ""))
            owner_email_tag = card.select_one(SELECTORS.get("owner_email", ""))

            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            size_text = size_tag.get_text(strip=True) if size_tag else ""
            website = website_tag["href"] if website_tag and website_tag.has_attr("href") else ""
            owner_name = owner_name_tag.get_text(strip=True) if owner_name_tag else ""
            owner_email = owner_email_tag.get_text(strip=True) if owner_email_tag else ""

            min_emp, max_emp = parse_employee_range(size_text)
            if min_emp is None or max_emp is None:
                # Cannot parse size; skip
                continue

            if not (MIN_EMPLOYEES <= max_emp <= MAX_EMPLOYEES):
                # Skip companies outside size filter
                continue

            # Validate email syntax
            email_valid_syntax = is_valid_email_syntax(owner_email)
            # Optionally, verify via API (uncomment if you have API key)
            email_verified = None
            # if email_valid_syntax and owner_email:
            #     email_verified = verify_email_api(owner_email)

            entries.append({
                "company_name": name,
                "company_size": size_text,
                "company_website": website,
                "owner_name": owner_name,
                "owner_email": owner_email,
                "email_valid_syntax": email_valid_syntax,
                "email_verified": email_verified
            })

            time.sleep(0.5)  # polite, avoid hammering server

        except Exception as e:
            print(f"Error processing company card: {e}")
            continue

    print(f"Scraped {len(entries)} entries matching size and with emails collected.")
    return entries

def save_to_csv(data, filename="startups_leads.csv"):
    fieldnames = [
        "company_name",
        "company_size",
        "company_website",
        "owner_name",
        "owner_email",
        "email_valid_syntax",
        "email_verified"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    print(f"Saved {len(data)} records to {filename}.")

if __name__ == "__main__":
    leads = scrape()
    if leads:
        save_to_csv(leads)
