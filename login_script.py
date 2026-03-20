import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys

EMAIL = "bakabdal@sutherlandglobal.com"
PASSWORD = "12345678"
INTERVAL = 5          # seconds between attempts

def login_attempt(attempt_number):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
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
        # Return False if we want to stop on failure, but we'll continue in loop
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    attempt = 0
    while True:
        attempt += 1
        login_attempt(attempt)
        time.sleep(INTERVAL)
