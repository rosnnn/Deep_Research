# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return bool(parsed.netloc) and parsed.netloc == base_domain and bool(parsed.scheme)

def get_links_from_url(base_url, max_links=3):
    try:
        response = requests.get(base_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"[!] Failed to fetch {base_url}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        base_domain = urlparse(base_url).netloc

        # Limit to content within the same article or related sections
        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href")
            full_url = urljoin(base_url, href)
            # Only follow links within the same Wikipedia article or its subsections
            if is_valid_url(full_url, base_domain) and "/wiki/Machine_learning" in full_url:
                links.add(full_url)
            if len(links) >= max_links:
                break

        return list(links)

    except Exception as e:
        print(f"[ERROR] {base_url} - {e}")
        return []

def extract_html_content(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"[!] Could not fetch {url}")
            return None
        return response.text
    except Exception as e:
        print(f"[ERROR] {url} - {e}")
        return None