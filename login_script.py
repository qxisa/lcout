import time
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

EMAIL = "bakabdal@sutherlandglobal.com"
PASSWORD = "12345678"
INTERVAL = 5          # seconds between attempts
MAX_ATTEMPTS = 1000   # set to None for unlimited

def login_attempt(attempt_number):
    temp_dir = tempfile.mkdtemp()

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://outlook.live.com/")
        wait = WebDriverWait(driver, 15)

        # Print the page title to see if we're on the correct page
        print(f"Page title: {driver.title}")

        # Optionally, print a snippet of page source for debugging (uncomment if needed)
        # print(driver.page_source[:500])

        # Many Outlook login pages use a different flow: first the "Sign in" button,
        # then the email field. Let's try to find the email field directly.
        # If not found, we might need to click a "Sign in" button first.

        # Try to locate the email field by multiple possible selectors
        email_selectors = [
            (By.NAME, "loginfmt"),
            (By.ID, "i0116"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.XPATH, "//input[@placeholder='Email, phone, or Skype']"),
            (By.XPATH, "//input[@aria-label='Email address']")
        ]

        email_field = None
        for by, value in email_selectors:
            try:
                email_field = wait.until(EC.presence_of_element_located((by, value)))
                print(f"Email field found with selector: {by}={value}")
                break
            except:
                continue

        if email_field is None:
            raise Exception("Email field not found with any selector")

        email_field.send_keys(EMAIL)

        # Next button could be different
        next_selectors = [
            (By.ID, "idSIButton9"),
            (By.ID, "next"),
            (By.XPATH, "//input[@value='Next']"),
            (By.XPATH, "//button[contains(text(),'Next')]")
        ]

        next_btn = None
        for by, value in next_selectors:
            try:
                next_btn = wait.until(EC.element_to_be_clickable((by, value)))
                break
            except:
                continue

        if next_btn is None:
            raise Exception("Next button not found")

        next_btn.click()
        time.sleep(2)  # wait for password field

        # Password field selectors
        password_selectors = [
            (By.NAME, "passwd"),
            (By.ID, "i0118"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.XPATH, "//input[@placeholder='Password']")
        ]

        password_field = None
        for by, value in password_selectors:
            try:
                password_field = wait.until(EC.presence_of_element_located((by, value)))
                break
            except:
                continue

        if password_field is None:
            raise Exception("Password field not found")

        password_field.send_keys(PASSWORD)

        # Sign in button
        signin_selectors = [
            (By.ID, "idSIButton9"),
            (By.ID, "submit"),
            (By.XPATH, "//input[@value='Sign in']"),
            (By.XPATH, "//button[contains(text(),'Sign in')]")
        ]

        signin_btn = None
        for by, value in signin_selectors:
            try:
                signin_btn = wait.until(EC.element_to_be_clickable((by, value)))
                break
            except:
                continue

        if signin_btn is None:
            raise Exception("Sign in button not found")

        signin_btn.click()
        time.sleep(3)  # allow the next page to load

        print(f"Attempt {attempt_number} at {time.ctime()} completed.")
        return True

    except Exception as e:
        print(f"Attempt {attempt_number} failed: {e}")
        return False

    finally:
        driver.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    attempt = 0
    while True:
        attempt += 1
        if MAX_ATTEMPTS and attempt > MAX_ATTEMPTS:
            print("Max attempts reached. Exiting.")
            break
        login_attempt(attempt)
        time.sleep(INTERVAL)
