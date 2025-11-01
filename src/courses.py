import time
import json
import re
from pathlib import Path
from typing import List, Dict

from bs4 import BeautifulSoup

COURSE_CODE_RE = re.compile(r"[A-Z]{4}\d{4}")


def parse_course_page(html: str) -> Dict:
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1")
    course_title = title.get_text(strip=True) if title else "Unknown course"

    units = None
    units_el = soup.find(string=re.compile("unit", re.IGNORECASE))
    if units_el and units_el.parent:
        units = units_el.parent.get_text(strip=True)

    # Example availability parsing (adjust to real DOM)
    availability = []
    for badge in soup.select(".availability, .badge-offering, .offered-in li"):
        availability.append(badge.get_text(strip=True))

    return {
        "course_name": course_title,
        "credits": units,
        "availability": availability,
    }


def scrape_course_list_from_degree(driver, degree_url: str, output_dir: Path, delay: float = 1.5) -> Path:
    """Given a degree URL, open it and try to find course links on that page.

    This is intentionally generic to avoid leaking any real university DOM.
    """
    driver.get(degree_url)
    time.sleep(delay)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    courses: List[Dict] = []

    # Example: course table with links
    for link in soup.select("a[href*='/course'], table.handbook-course-listing a"):
        href = link.get("href")
        code_text = link.get_text(strip=True)

        # try to detect course code
        code_match = COURSE_CODE_RE.search(code_text or "")
        course_code = code_match.group(0) if code_match else code_text

        if not href:
            continue

        # visit the course page
        driver.get(href)
        time.sleep(delay)
        course_data = parse_course_page(driver.page_source)
        course_data["_id"] = course_code
        courses.append(course_data)

        # go back to degree page
        driver.back()
        time.sleep(0.5)

    output_dir.mkdir(exist_ok=True, parents=True)
    out_path = output_dir / "courses.json"
    out_path.write_text(json.dumps(courses, indent=4), encoding="utf-8")
    return out_path