from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/kitchensink.html")

        print(driver.find_element(By.ID, "mousehover").text)
        print(driver.find_element(By.NAME, "enter-name").get_attribute("id"))
        print(driver.find_element(By.XPATH, '//*[@id="bmwcheck"]').get_attribute("value"))
        print(driver.find_element(By.XPATH, '//input[@value="Yet Another button"]').get_attribute("type"))
        print(driver.find_element(By.XPATH, '//*[@id="multiple-select-example"]/option[1]').text)
    except Exception as e:
        print('Exception occured: ', e)
    finally:
        if driver:
            driver.close()
