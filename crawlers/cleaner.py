# cleaner.py
from bs4 import BeautifulSoup
import re

def clean_html(html):
    """
    Extracts clean readable text from raw HTML, removing navigational and structural elements.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove script, style, navigational, and structural elements
    for element in soup(["script", "style", "noscript", "nav", "header", "footer", "aside", "form", "table"]):
        element.decompose()

    # Remove specific Wikipedia navigational elements
    for element in soup.find_all(class_=["mw-jump-link", "vector-menu", "vector-tabs", "mw-editsection", "infobox"]):
        element.decompose()

    # Get text
    text = soup.get_text(separator="\n")

    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)

    # Remove excessive newlines and Wikipedia clutter
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"Jump to content|Main menu|move to sidebar|hide|Navigation|Contribute|Special pages|Search|Appearance|Donate|Create account|Log in|Personal tools|Pages for logged out editors|learn more|Contributions|Talk|Edit|References|External links|Categories|From Wikipedia, the free encyclopedia|For the journal, see.*?\.|\"Statistical learning\" redirects here.*?\.", "", text)
    text = re.sub(r"\[\d+\]|\(Full article...\)|Recently featured:.*", "", text)

    return text.strip()