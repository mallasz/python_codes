# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def teszt_not_negative(param):
    """
    tests in the event of the param is not a negative number
    :param: number or text
    :return: result as string
    """
    r.clear()
    r.send_keys(param)
    submit_button.click()
    return driver.find_element(By.ID, "result").text


def teszt_negative(param):
    """
    tests in the event of the param is a negative number
    :param: number or text
    :return: result as string
    """
    r.clear()
    r.send_keys(param)
    submit_button.click()
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()
    return alert_text


def load_page():
    driver.get(base_url)


base_url = "http://selenium.oktwebs.training360.com/7709_zarovizsga/kor_terulete.html"

driver = None
if __name__ == '__main__':

    try:

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        load_page()

        r = driver.find_element(By.ID, "r")
        submit_button = driver.find_element(By.ID, "submit")

        # TC1
        assert teszt_not_negative(10) == "314"

        # TC2
        assert teszt_negative(-5) == "A kör sugara nem lehet negatív szám!"

        # TC3
        assert teszt_not_negative("abrakadabra") == "NaN"

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
