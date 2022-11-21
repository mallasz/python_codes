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

    URL = "http://selenium.oktwebs.training360.com/5201_kepesitovizsga/pitagorasz.html"
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
        Fills the input fields with the given value according the given strategy and locator.
        :param by_strategy: By.ID, By.XPATH, etc.
        :param locator: locator of the strategy
        :param value: value to fill
        :return: None
        """
        element = self.driver.find_element(by_strategy, locator)
        element.clear()
        element.send_keys(value)

    def calculate_triangle(self, a, b):
        """
        Calculate the third side of the triangle.
        :param a: the length of the a side
        :param b: the length of the b side
        :return: None
        """
        self.fill_input(By.ID, "a", a)
        self.fill_input(By.ID, "b", b)
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

    def get_result(self):
        """
        Gets the third side of the triangle
        :return: String
        """
        return self.driver.find_element(By.ID, "result").text


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


# correct fill in
def test_pithagorasz_tc001(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(3)  # wait for load
    page.calculate_triangle(3, 4)
    assert page.get_result() == "5.00"
    sleep(3)  # see the result


# fill in with invalid "a" value
def test_pithagorasz_tc002(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(3)  # wait for load
    page.calculate_triangle("a", 4)
    assert page.get_result() == "NaN"
    sleep(3)  # see the result


# fill in with invalid "b" value
def test_pithagorasz_tc003(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(3)  # wait for load
    page.calculate_triangle(3, "b")
    assert page.get_result() == "NaN"
    sleep(3)  # see the result


# empty fields
def test_pithagorasz_tc004(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(3)  # wait for load
    page.calculate_triangle("", "")
    assert page.get_result() == "NaN"
    sleep(3)  # see the result
