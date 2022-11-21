from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def get_element_id(number):
    """
    Convert element number to text
    :param number: the number
    :return: str
    """
    return f'element{number}'


def visit_elements():
    """
    Visits elements with ID elementX from 1 to N
    :return: number of elements found
    """
    element_number = 1
    while does_exist(get_element_id(element_number)):
        element_number += 1
    return element_number - 1


def does_exist(html_id):
    """
    Check that the element does exist.
    :param html_id: The element id in the HTML document.
    :return: Bool
    """
    try:
        driver.find_element(By.ID, html_id)
        return True
    except NoSuchElementException as e:
        return False


def is_correct_label(html_id):
    """
    Check that the button id matches the label's text.
    :param html_id: ID of the button
    :return: Bool
    """
    if not does_exist("result"):
        print("A result label nem létezik")
        return False
    result_text = driver.find_element(By.ID, "result").text
    if result_text != f'{html_id} was clicked':
        print("A label szövege nem megfelelő")
        return False
    print("A label szövege megfelelő")
    return True


def get_first_button_id():
    """
    Checks if the element is a button and returns with the id as a string.
    :return: str if found, None if not found
    """
    try:
        x = driver.find_element(By.XPATH, "//button")
        html_id = x.get_attribute("id")
        return html_id
    except:
        return None


def label_check():
    """
    If there is at least one button on the HTML page, clicks the first one,
    and checks the result's text.
    :return: bool
    """
    html_id = get_first_button_id()
    if html_id is None:
        return None
    driver.find_element(By.ID, html_id).click()
    return is_correct_label(html_id)


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://selenium.oktwebs.training360.com/trickyelements.html")
    visit_elements()
    result = label_check()
    if result is True:
        print("sikeres teszt")
    elif result is None:
        print("nem volt gomb az oldalon, blokkolt teszt")
    else:
        print("sikertelen teszt")
    driver.close()
