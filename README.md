# University Handbook Scraper (Sanitized)

This project is an **educational** example showing how to scrape a university handbook-style website to collect **degrees** and **courses** into JSON files.

⚠️ **Important**
- This repo does **not** contain any data from the University of Newcastle or any other real institution.
- To run it against a real site, create your own `config.py` (see `config.example.py`) with your URLs and driver path.
- Check the target website’s Terms of Use and robots.txt before scraping.
- Do **not** publish scraped data that you don't own.

## How it works
1. We bootstrap a Selenium Chrome driver (headless, JS optional).
2. We visit the "degrees" listing page and extract degree names + links.
3. We visit each degree page and (optionally) collect linked courses.
4. We dump everything in `outputs/` as JSON.

## Files
- `config.example.py` – template for your local settings.
- `src/utils.py` – Selenium driver builder.
- `src/degrees.py` – scrapes degree pages.
- `src/courses.py` – scrapes course pages from a degree.
- `src/main.py` – entry point.

## Running
```bash
cp config.example.py config.py   # then edit
python -m src.main
```