from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import re

def find_business_leads(query, max_results=10):
    """
    Finds business websites using DuckDuckGo and scrapes them for contact info.
    """
    print(f"Searching for business leads for: {query}")
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=max_results)]

    leads = []

    for res in results:
        url = res.get('href')
        title = res.get('title')

        if url:
            print(f"Scraping: {url}")
            contact_info = scrape_contact_info(url)
            leads.append({
                'source': 'Web',
                'name': title,
                'url': url,
                'email': contact_info.get('email'),
                'description': res.get('body')
            })

    return leads

def scrape_contact_info(url):
    """
    Very basic scraper to find emails on a page.
    """
    info = {'email': None}
    try:
        response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            # Simple regex for emails
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
            if emails:
                # Filter out common false positives if any, or just take the first
                unique_emails = list(set(emails))
                # Basic filter to avoid things like .png, .jpg in email-like strings
                filtered = [e for e in unique_emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
                if filtered:
                    info['email'] = filtered[0]
    except Exception:
        pass

    return info

if __name__ == "__main__":
    # Test
    results = find_business_leads("digital marketing agency London", max_results=2)
    for lead in results:
        print(lead)
