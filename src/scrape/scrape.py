import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from dotenv import load_dotenv
_ = load_dotenv()

from auth import handle_login
from datetime import date
import time


PAYCHECK_PAGE_URL = "https://www.prat.idf.il/השכר-שלי/תלוש-השכר"
PAYCHECK_DOWNLOAD_URL_TEMPLATE = "https://www.prat.idf.il/umbraco/surface/paychecks/GetPaycheckFile?paycheckNumber=1&month={month}&year={year}&populationType=2"
def create_driver():
    appdata_local_path = os.getenv('LOCALAPPDATA')
    options = Options()
    
    # profile to maintain session stuff like auth
    profile_name = "PaycheckScraperProfile"
    options.add_argument(f"--user-data-dir={appdata_local_path}\\Google\\Chrome\\User Data\\{profile_name}")

    prefs = {
        "download.prompt_for_download": False,
        "download.default_directory": os.path.abspath("./my_paychecks"),
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    } 
    options.add_experimental_option("prefs", prefs)
    show_browser = os.getenv('SHOW_BROWSER', 'true').lower() == 'true'
    if not show_browser:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080") # Headless by default has small window size
    
    service = Service(executable_path="chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def enter_paycheck_page(driver: webdriver.Chrome):
    driver.get(PAYCHECK_PAGE_URL)
    if driver.current_url.startswith("https://www.prat.idf.il/?returnUrl="):
        handle_login(driver)
        _ = WebDriverWait(driver, 30).until(EC.url_matches(PAYCHECK_PAGE_URL))

def get_download_link(year: int, month: int) -> str:
    return PAYCHECK_DOWNLOAD_URL_TEMPLATE.format(year=year, month=month)

def download_file(driver: webdriver.Chrome, year: int, month: int, session: requests.Session):
    download_link = get_download_link(year, month)

    response = session.get(download_link)
    content_type = response.headers.get('Content-Type', '')
    if 'application/pdf' not in content_type:
        raise Exception(f"Failed to download paycheck file for {month}/{year}")

    download_path = os.path.abspath("./my_paychecks")
    target_folder = os.path.join(download_path, str(year))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    final_path = os.path.join(target_folder , f"תלוש שכר {month:02}.{year % 100}.pdf")
    with open(final_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded paycheck to {final_path}")

def download_files(driver: webdriver.Chrome):
    today = date.today()
    year = today.year
    month = today.month
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    while True:
        try:
            download_file(driver, year, month, session)
            # Move to previous month
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        except Exception as e:
            print(f"No more paychecks found or error occurred: {e}")
            break

    

def scrape():
    driver = create_driver()
    enter_paycheck_page(driver)
    download_files(driver)

    driver.quit()


if __name__ == "__main__":
    scrape()

