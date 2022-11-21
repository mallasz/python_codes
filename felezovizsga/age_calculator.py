# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def get_age_in_different_units(age, html_id):
    """
    gets the calculated age in the given unit
    :param age: age to convert
    :param html_id: id of the result field
    :return: calculated age result as a string
    """
    age_input = driver.find_element(By.ID, 'age')
    button_input = driver.find_element(By.ID, 'submit')
    result_element = driver.find_element(By.ID, html_id)
    age_input.clear()
    age_input.send_keys(str(age))
    button_input.click()
    return result_element.text


base_url = "http://selenium.oktwebs.training360.com/r2d2_felezovizsga/age_calculator.html"
driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(base_url)

        # TC_001
        assert get_age_in_different_units(39, 'minutes') == '20512440'
        # TC_002
        assert get_age_in_different_units('', 'seconds') == '0'
        # TC_003
        assert get_age_in_different_units(112, 'seconds') == '3534451200'

    except Exception as e:
        print('Exception occured: ', e)

    finally:
        if driver:
            driver.close()
