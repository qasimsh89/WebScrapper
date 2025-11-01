from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def build_driver(chromedriver_path: str, headless: bool = True, disable_js: bool = True):
    """Create and return a configured Selenium Chrome driver."""
    chrome_options = Options()
    if headless:
        # new headless mode
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1280,720")

    if disable_js:
        # 2 means block
        chrome_options.add_experimental_option(
            "prefs",
            {"profile.managed_default_content_settings.javascript": 2}
        )

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    return driver