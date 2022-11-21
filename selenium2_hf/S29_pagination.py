from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.common.keys import Keys
import csv

driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/pagination.html")

        lst = []

        while True:
            rows = driver.find_elements(By.XPATH, '//table[@id="contacts-table"]/tbody/tr')
            for row in rows:
                personal_data = row.find_elements(By.TAG_NAME, "td")
                if personal_data[1].text[0] == "A":
                    dictionary = {"Id": personal_data[0].text,
                                  "First name": personal_data[1].text,
                                  "Second name": personal_data[2].text,
                                  "Surname": personal_data[3].text,
                                  "Second Surname": personal_data[4].text,
                                  "Birth Date": personal_data[5].text}
                    lst.append(dictionary)
            next_button = driver.find_element(By.ID, "next")
            if not next_button.is_enabled():
                break
            else:
                next_button.click()

        if len(lst) > 0:
            with open('personaldata.csv', 'w', newline='') as csvfile:
                wr = csv.writer(csvfile, delimiter=',')
                wr.writerow(lst[0].keys())  # creates CSV header using the dictionary keys
                for d in lst:
                    wr.writerow(d.values())

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
