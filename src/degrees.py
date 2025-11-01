import time
import json
from pathlib import Path
from typing import List, Dict

from bs4 import BeautifulSoup


def parse_degrees_html(html: str, base_url: str) -> List[Dict]:
    """Parse the degree listing HTML and return a list of degree dicts.

    NOTE: You must adjust the CSS selectors below to match your real target site.
    """
    soup = BeautifulSoup(html, "html.parser")
    degrees = []

    # Example selector (generic):
    # <div class="degree-card"><a href="/degrees/bachelor-of-x">Bachelor of X</a></div>
    for card in soup.select(".degree-card a, .degree-title a, .uon-card-content a"):
        title = card.get_text(strip=True)
        href = card.get("href", "")
        if not title:
            continue
        degrees.append(
            {
                "degree_id": href.rsplit("/", 1)[-1] or title.lower().replace(" ", "-"),
                "degree_name": title,
                "degree_url": href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/"),
            }
        )

    return degrees


def scrape_degrees(driver, base_url: str, output_dir: Path, delay: float = 1.5) -> Path:
    """Visit the degrees page with Selenium, parse, and save to JSON."""
    driver.get(base_url)
    time.sleep(delay)  # give it a moment
    html = driver.page_source

    degrees = parse_degrees_html(html, base_url)

    output_dir.mkdir(exist_ok=True, parents=True)
    out_path = output_dir / "degrees.json"
    out_path.write_text(json.dumps(degrees, indent=4), encoding="utf-8")
    return out_path