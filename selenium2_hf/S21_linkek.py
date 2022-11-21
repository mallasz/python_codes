# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com")

        links = driver.find_elements(By.TAG_NAME, "a")
        urls = [link.get_attribute("href") for link in links]
        print(f'Talált linkek száma: {len(urls)}')

        with open("result.txt", "w") as file:
            file.write("\n".join(urls))

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
