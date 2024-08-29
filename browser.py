import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def setup_driver():
    options = FFOptions()
    options.binary_location = "/home/david/Downloads/firefox/firefox"
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    service = FFService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1920, 1080)
    return driver


def inject_css(driver, css):
    js_script = (
        f"var style = document.createElement('style'); style.textContent = `{css}`; document.head.appendChild(style);"
    )
    driver.execute_script(js_script)


def screenshot_with_styles(driver, url, css_to_inject, domain):
        # Load the URL
        driver.get(url)
        print(f"Loaded URL: {url}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(0.5)
        driver.save_screenshot(f"{domain}_before.png")
        inject_css(driver, css_to_inject)
        time.sleep(0.5)
        driver.save_screenshot(f"{domain}_after.png")
