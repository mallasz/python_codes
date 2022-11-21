import pytest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys
import traceback


class Page:
    URL = "http://selenium.oktwebs.training360.com/7904_potzarovizsga/calculator.html"
    op_dict = {'+': 'add', '-': 'subtract', '*': 'multiply', '/': 'divide', '=': 'equals', '%':'percent'}

    def __init__(self, driver):
        self.driver = driver

    def visit_page(self):
        self.driver.get(self.URL)

    def press_calculator_key(self, button):
        self.driver.find_element(By.CLASS_NAME, f"key-{button}").click()

    def press_numbers(self, number):
        for button in str(number):
            if button == '.':
                self.press_calculator_key('dot')
            else:
                self.press_calculator_key(button)

    def clear(self):
        self.press_calculator_key('clear')

    def operation(self, op):
        self.press_calculator_key(self.op_dict[op])

    def get_result(self):
        return self.driver.find_element(By.CLASS_NAME, "auto-scaling-text").text.replace(" ","")

    def calculate(self, *args):
        for arg in args:
            if arg in self.op_dict.keys():
                self.operation(arg)
            else:
                self.press_numbers(arg)






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
    return Page(driver)


class Calculator:

    def __init__(self):
        self.ans=0
        self.displayed=0
        self.operator=None

    def press_numbers(self, number):
        self.displayed=number

    def operation(self, op):
        if op == '%':
            self.displayed/=100
            return
        if self.operator is None or self.operator == '=':
            self.ans=self.displayed
        elif self.operator == '+':
            self.ans+=self.displayed
            self.displayed=self.ans
        elif self.operator == '-':
            self.ans-=self.displayed
            self.displayed=self.ans
        elif self.operator == '/':
            self.ans/=self.displayed
            self.displayed=self.ans
        elif self.operator == '*':
            self.ans*=self.displayed
            self.displayed=self.ans
        self.operator=op

    def calculate(self, *args):
        for arg in args:
            if arg in ['+','-','/','*','%']:
                self.operation(arg)
            else:
                self.press_numbers(arg)

    def get_result(self):
        return self.displayed


def calculate_net_sum(*args):
    net_prices = 0
    for i in range(len(args)):
        net_prices += args[i]
    return net_prices



def test_TC1(driver, page):
    page.visit_page()
    calc=Calculator()
    page.calculate(1000,"+",3000,"=")
    calc.calculate(1000,"+",3000,"=")
    print(calc.get_result())
    assert page.get_result() == '4000'
    page.calculate("*",27,'%',"=")
    assert page.get_result() == '1080'
    time.sleep(5)
