import requests
from scraper.logger import log

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        log.warning(f"Fetch failed: {e}")
        return None