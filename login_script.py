import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

EMAIL = "bakabdal@sutherlandglobal.com"
PASSWORD = "12345678"
INTERVAL = 5          # seconds between attempts
MAX_ATTEMPTS = 1000   # set to None for unlimited

def login_attempt(attempt_number):
    # Create a temporary directory for user data to avoid permission issues
    temp_dir = tempfile.mkdtemp()

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    # Essential headless options
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")

    # Stealth options to avoid detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Use webdriver-manager to get correct chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://outlook.live.com/")
        time.sleep(3)

        email_field = driver.find_element(By.NAME, "loginfmt")
        email_field.send_keys(EMAIL)

        next_btn = driver.find_element(By.ID, "idSIButton9")
        next_btn.click()
        time.sleep(2)

        password_field = driver.find_element(By.NAME, "passwd")
        password_field.send_keys(PASSWORD)

        signin_btn = driver.find_element(By.ID, "idSIButton9")
        signin_btn.click()
        time.sleep(2)

        print(f"Attempt {attempt_number} at {time.ctime()} completed.")
        return True
    except Exception as e:
        print(f"Attempt {attempt_number} failed: {e}")
        return False
    finally:
        driver.quit()
        # Clean up temporary directory
        import shutil
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
