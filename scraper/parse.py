from bs4 import BeautifulSoup
import re
from datetime import datetime, timezone
from scraper.fetch import fetch_page

def parse_school_page(school_meta):
    url = school_meta["url"]
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    doc = {
        "school_code": school_meta["school_code"],
        "school_name": school_meta["school_name"],
        "source_url": url,
        "scraped_at": datetime.now(timezone.utc),
        "exam_year": 2025,
        "exam_type": "ACSEE",
        "candidates": [],
        "subject_summary": [],
        "school_summary": {}
    }

    tables = soup.find_all("table")

    for table in tables:
        headers_row = table.find("tr")
        if not headers_row:
            continue

        col_texts = [th.get_text(strip=True).upper() for th in headers_row.find_all(["th","td"])]

        # Candidate table
        if any(col in col_texts for col in ["CNO","CANDIDATE NO","REG NO"]):
            for row in table.find_all("tr")[1:]:
                cells = [td.get_text(strip=True) for td in row.find_all(["td","th"])]
                if len(cells) < 3:
                    continue

                candidate = {
                    "candidate_no": cells[0],
                    "sex": cells[1],
                    "aggregate": cells[2],
                    "division": cells[3] if len(cells) > 3 else None,
                    "subjects": {}
                }

                for i, col in enumerate(col_texts[4:], start=4):
                    if col and i < len(cells):
                        candidate["subjects"][col] = cells[i]

                doc["candidates"].append(candidate)

    return doc