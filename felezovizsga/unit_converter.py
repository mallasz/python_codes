# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def get_converted_value(number, from_unit):
    """
    Fills in the form's number and unit inputs with the given values and returns the converted values as a string
    :param number: value to convert into a string
    :param from_unit: original unit
    :return: result as a string
    """
    number_element = driver.find_element(By.ID, 'number')
    unit_element = driver.find_element(By.ID, 'unit')
    result_element = driver.find_element(By.CLASS_NAME, 'conversion')
    number_element.clear()
    unit_element.clear()
    number_element.send_keys(str(number))
    unit_element.send_keys(str(from_unit))
    return result_element.text


# tc_001
def tc_001():
    result = get_converted_value(112, 'meter')
    assert result == '367.45 FOOT'


# tc_002
def tc_002():
    result = get_converted_value(8, 'oz')
    assert result == '236.56 MILLILITER'


# tc_003
def tc_003():
    result = get_converted_value(1, 'gallon')
    assert result == '3.79 LITER'


base_url = "http://selenium.oktwebs.training360.com/r2d2_felezovizsga/unit_converter.html"
driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(base_url)

        tc_001()
        tc_002()
        tc_003()

    except Exception as e:
        print('Exception occured: ', e)

    finally:
        if driver:
            driver.close()
