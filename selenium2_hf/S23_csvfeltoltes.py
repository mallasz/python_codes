import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import csv
import os
import filecmp


def fill_in(html_id, content=None):
    """
    fills the input field with the given content after clearing the filed
    :param html_id: the id of the target input field
    :param content: string to be filled in
    :return: the webelement object
    """
    element = driver.find_element(By.ID, html_id)
    element.clear()
    if content:
        element.send_keys(content)
    return element


driver = None
if __name__ == '__main__':
    try:
        # change the download directory to the current directory to make possible the comparison of files
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory": os.path.abspath(os.getcwd())}
        chromeOptions.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
        driver.get("http://selenium.oktwebs.training360.com/another_form.html")

        with open("table_in.csv", "r", newline='', encoding='utf-8') as csvfile:
            table_reader = csv.reader(csvfile, delimiter=',')
            next(table_reader)  # skip the header
            lst = []
            submit_button = driver.find_element(By.ID, "submit")
            for row in table_reader:
                # fill in the fields
                fill_in("fullname", row[0])
                fill_in("email", row[1])
                fill_in("dob", row[2])
                fill_in("phone", row[3])
                lst.append(row)
                submit_button.click()
            driver.find_element(By.XPATH, '// button[text() = "Export HTML table to CSV file"]').click()
            time.sleep(5)  # waiting for download the CSV file
            assert filecmp.cmp("table_in.csv", "table.csv")  # compare the original and the downloaded files
            os.remove(
                "table.csv")  # delete the downloaded file, otherwise the name would not be the same at the next run

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
