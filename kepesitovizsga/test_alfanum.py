# imports
import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver


class Page:
    """
    Using the Page Object Model, this is the Page side. Test cases are using this object from the outside
    """

    URL = "http://selenium.oktwebs.training360.com/5201_kepesitovizsga/alfanum.html"
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

    def fill_input(self, by_strategy, locator, value):
        """
        Fills an input field given be a strategy-locator pair with the given value.
        If value is an empty string, use a tricky method to delete content. (JS must be triggered)
        :param by_strategy: By.ID, By.XPATH, etc.
        :param locator: locator of the strategy
        :param value: value to fill
        :return: None
        """
        element = self.driver.find_element(by_strategy, locator)
        if len(value) > 0:
            element.clear()
            element.send_keys(value)
        else:
            for i in range(len(element.get_attribute('value'))):
                element.send_keys(Keys.BACKSPACE)

    def fill_login(self, s):
        """
        Fill the login form
        :param s: string to input
        :return: None
        """
        self.fill_input(By.ID, 'title', s)

    def get_error_message(self):
        """
        Finds and returns the error message. Returns None if there was no error.
        :return: str or None
        """
        try:
            element = self.driver.find_element(By.XPATH, "//span[@class='error active']")
            return element.text
        except NoSuchElementException:
            return None

    def fill_and_get_error_message(self, s):
        self.fill_login(s)
        sleep(2)
        return self.get_error_message()


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


# fill in with valid input
def test_alfanum_tc001(driver: WebDriver, page: Page):
    page.visit_page()  # load page
    sleep(1)  # wait for load

    assert page.fill_and_get_error_message("abcd1234") is None  # TC001's data
    sleep(2)  # see the result


# fill in with invalid input
def test_alfanum_tc002(driver: WebDriver, page: Page):
    page.visit_page()  # load page
    sleep(1)  # wait for load

    assert page.fill_and_get_error_message("teszt233@") == "Only a-z and 0-9 characters allowed"  # TC002's data
    # specification has a '.' at the end
    sleep(2)  # see the result


# too short input
def test_alfanum_tc003(driver: WebDriver, page: Page):
    page.visit_page()  # load page
    sleep(1)  # wait for load

    assert page.fill_and_get_error_message("12cd") == "Login should be at least 8 characters; you entered 4"
    # TC003's data
    sleep(2)  # see the result


# empty input field after deletion
def test_alfanum_tc004(driver: WebDriver, page: Page):
    page.visit_page()  # load page
    sleep(1)  # wait for load

    page.fill_login("12cd")
    assert page.fill_and_get_error_message("") == "Cannot be empty"
    # TC004's data
    sleep(2)  # see the result
