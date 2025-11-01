from pathlib import Path

try:
    import config  # your local, untracked config
except ImportError:
    raise SystemExit("Create config.py from config.example.py first.")


from .utils import build_driver
from .degrees import scrape_degrees
from .courses import scrape_course_list_from_degree


def main():
    output_dir = Path(config.OUTPUT_DIR)
    driver = build_driver(
        chromedriver_path=config.CHROMEDRIVER_PATH,
        headless=config.HEADLESS,
        disable_js=config.DISABLE_JS,
    )

    # 1) scrape degrees
    degrees_path = scrape_degrees(driver, config.BASE_DEGREE_URL, output_dir, delay=config.REQUEST_DELAY_SEC)
    print(f"Degrees saved to {degrees_path}")

    # 2) optionally, scrape courses from the FIRST degree only (to avoid hammering a site)
    degrees = []
    try:
        import json
        degrees = json.loads(degrees_path.read_text(encoding="utf-8"))
    except Exception:
        pass

    if degrees:
        first_degree_url = degrees[0]["degree_url"]
        courses_path = scrape_course_list_from_degree(
            driver, first_degree_url, output_dir, delay=config.REQUEST_DELAY_SEC
        )
        print(f"Courses saved to {courses_path}")

    driver.quit()


if __name__ == "__main__":
    main()