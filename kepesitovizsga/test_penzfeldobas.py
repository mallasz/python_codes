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

    URL = "http://selenium.oktwebs.training360.com/5201_kepesitovizsga/penzfeldobas.html"
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

    def press_coin_button(self):
        """
        Presses the button to flip a coin
        :return: None
        """
        self.driver.find_element(By.ID, 'submit').click()

    def get_last_result(self):
        """
        Returns the result of the last flip
        :return: str ("fej" or "írás")
        """
        return self.driver.find_element(By.ID, 'lastResult').text

    def get_results(self):
        """
        Returns the entire history, as a list
        :return: list of strings
        """
        return [element.text for element in self.driver.find_elements(By.XPATH, "//ul[@id='results']/li")]


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


def test_flip_tc001(driver: WebDriver, page: Page):
    """
    TC001 check the last result and the history of the coin flips:
    :param driver:
    :param page:
    :return:
    """
    page.visit_page()  # load page
    sleep(3)  # wait for load

    for i in range(20):  # press the button 20 times
        page.press_coin_button()

    last_flip_result = page.get_last_result()  # get the last flip
    history = page.get_results()  # get the entire history
    assert last_flip_result == history[-1]  # the last element in history should be the same as the last flip

    sleep(3)  # see the result on screen


def test_flip_tc002(driver: WebDriver, page: Page):
    """
    TC002 check if the random generator gives sufficiently random values
    The specification asks for the number of heads to be between 45-55 for 100 flips, which often fails.
    :param driver:
    :param page:
    :return:
    """
    numbers_of_heads = []  # collect the number of heads in the tests
    for test_number in range(10):  # do 10 experiments, and get the average number of heads
        page.visit_page()  # load (or reload) page
        sleep(1)  # wait for load

        for flips in range(100):  # flip the coin 100 times
            page.press_coin_button()

        history = page.get_results()  # get the entire history
        number_of_heads = sum([1 for flip in history if flip == 'fej'])  # calculate the number of heads
        # to do this, construct a list using a list comprehension that has a 1 for every head in the history
        # then get its sum
        numbers_of_heads.append(number_of_heads)  # store it for later use
        assert 45 <= number_of_heads <= 55  # the number of heads should be between 45 and 55 (many times it's not)
        # assert 35 <= number_of_heads <= 65  # RNG is not that good

    # calculate average
    average_heads = sum(numbers_of_heads) / len(numbers_of_heads)
    # check it
    assert 45 <= average_heads <= 55
    # print("Number of heads: ", numbers_of_heads)  # just print it to know the result
    # print(f"Average number of heads: {average_heads")  # print the average
