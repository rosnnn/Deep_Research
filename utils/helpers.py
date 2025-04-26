# utils/helpers.py

import re
from bs4 import BeautifulSoup

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def deduplicate_results(pages):
    seen = set()
    unique = []
    for page in pages:
        if page['url'] not in seen:
            seen.add(page['url'])
            unique.append(page)
    return unique
