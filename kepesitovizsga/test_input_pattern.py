# imports
import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver


class Page:
    """
    Using the Page Object Model, this is the Page side. Test cases are using this object from the outside
    """

    URL = "http://selenium.oktwebs.training360.com/5201_kepesitovizsga/input-pattern.html"
    """
    URL of the page to load and test
    """

    def __init__(self, driver: WebDriver):
        """
        A simple constructor
        :param driver: a WebDriver object to use
        """
        self.driver = driver

    def visit_page(self):
        """
        Load the page
        :return: None
        """
        self.driver.get(self.URL)

    def fill_input_field(self, comment, value):
        """
        Finds the input element given by the comment (description) in the same table line. Clears it
        fills it with the given value character by character, and returns the resulting value.
        :param comment: Text next to the input field.
        :param value: Value to fill.
        :return: str (value of the input field)
        """
        element = self.driver.find_element(By.XPATH, f"//td[text()='{comment}']/../td[2]/input")
        element.clear()
        for character in value:
            element.send_keys(character)
        return element.get_attribute('value')


@pytest.fixture()
def driver():
    """
    Creates and returns a new Selenium webdriver.
    After the caller quits, yield gets back here, and the driver (and the browser window) quits.
    :return: the driver
    """
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        yield driver
    finally:
        if driver:
            driver.close()


@pytest.fixture()
def page(driver):
    """
    A fixture to create and return a Page object
    :param driver:
    :return: Page
    """
    return Page(driver)


TEST_STRING = 'ab1ef2ij3op4uv5'


# ALPHA ONLY
def test_pattern_tc001(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(1)  # wait for load

    assert page.fill_input_field("ALPHA ONLY", TEST_STRING) == 'abefijopuv'
    sleep(2)  # see the result


# NUMBER ONLY
def test_pattern_tc002(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(1)  # wait for load

    assert page.fill_input_field("NUMBER ONLY", TEST_STRING) == '12345'
    sleep(2)  # see the result


# ALPHANUMERIC ONLY
def test_pattern_tc003(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(1)  # wait for load

    assert page.fill_input_field("ALPHANUMERIC ONLY", TEST_STRING) == 'ab1ef2ij3op4uv5'
    sleep(2)  # see the result


# VOWEL ONLY
def test_pattern_tc004(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(1)  # wait for load

    assert page.fill_input_field("VOWELS ONLY", TEST_STRING) == 'aeiou'
    sleep(2)  # see the result
