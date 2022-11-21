from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def does_exist(html_id):
    try:
        driver.find_element(By.ID, html_id)
        return True
    except NoSuchElementException as e:
        return False


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("http://selenium.oktwebs.training360.com/trickyelements.html")

print("Létezik" if does_exist("nemletezik") else "Nem létezik")

driver.close()
