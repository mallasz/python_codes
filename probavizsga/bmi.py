from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def fill_form(height, weight):
    """
    fills the form with the given parameters
    :param height:
    :param weight:
    :return: None
    """
    h = driver.find_element(By.ID, "height")
    h.clear()
    h.send_keys(height)
    driver.find_element(By.XPATH, '//*[@id="heightunits"]/*[@value="metres"]').click()
    w = driver.find_element(By.ID, "weight")
    w.clear()
    w.send_keys(weight)
    driver.find_element(By.XPATH, '//*[@id="weightunits"]/*[@value="kg"]').click()
    driver.find_element(By.XPATH, '//input[@value="computeBMI"]').click()


def get_results():
    """
    Gets and returns with the calculated BMI results
    :return: Tuple with the numerical value first, and then the comment
    """
    output = driver.find_element(By.XPATH, '//h1/span[@id="output"]/..').text
    comment = driver.find_element(By.XPATH, '//h2/span[@id="comment"]/..').text
    return output, comment


def test_case(height, weight, expected_output, expected_comment):
    """
    Gets the testcase inputs to fill the form, and compares the results with expected values
    :param height:
    :param weight:
    :param expected_output:
    :param expected_comment:
    :return: None
    """
    fill_form(height, weight)
    output, comment = get_results()
    assert expected_output == output
    assert expected_comment == comment


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://selenium.oktwebs.training360.com/probavizsga/bmi.html")

    test_case(171, 45, 'Your BMI is: 15', 'This means you are: Underweight')
    test_case(185, 65, 'Your BMI is: 19', 'This means you are: Normal')

    driver.close()
