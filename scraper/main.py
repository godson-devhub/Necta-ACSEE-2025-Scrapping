import time
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
from scraper.config import INDEX_URL, DELAY_SECONDS
from scraper.logger import log
from scraper.fetch import fetch_page
from scraper.parse import parse_school_page
from scraper.mongo import get_mongo_collection

def get_school_links():
    html = fetch_page(INDEX_URL)
    if not html:
        raise RuntimeError("Could not fetch index page.")

    soup = BeautifulSoup(html, "html.parser")
    schools = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "results/" in href:
            code = a_tag.get_text(strip=True)

            full_url = urljoin(INDEX_URL, href)

            schools.append({
                "school_code": code,
                "school_name": code,
                "url": full_url
            })

    return schools

def main(mongo_uri, demo=False):
    schools = get_school_links()
    if demo:
        schools = schools[:5]

    collection = get_mongo_collection(mongo_uri)

    for school in schools:
        doc = parse_school_page(school)
        if doc:
            collection.update_one(
                {"school_code": doc["school_code"]},
                {"$set": doc},
                upsert=True
            )
            log.info(f"Stored {doc['school_code']}")
        time.sleep(DELAY_SECONDS)