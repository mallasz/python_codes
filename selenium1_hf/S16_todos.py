from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/todo.html")

        lst = driver.find_elements(By.CLASS_NAME, "done-false")
        for i in lst:
            print(i.text)

    except Exception as e:
        print('Exception occured: ', e)

    finally:
        if driver:
            driver.close()
