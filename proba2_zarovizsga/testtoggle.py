# imports

import pytest
import traceback
import random
import requests
import csv
import os
import math
import filecmp
import re
from time import sleep
from functools import reduce
from datetime import datetime, date, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver


class Page:
    URL = "http://selenium.oktwebs.training360.com/7904_potzarovizsga/toggle.html"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        print(type(driver))

    def visit_page(self):
        self.driver.get(self.URL)

    def toggle(self):
        element = self.driver.find_element(By.XPATH, '//label[@for="toggle"]')
        element.click()
        #self.driver.execute_script('document.getElementById("toggle").click()')


    def fill_input(self, by_strategy, locator, value):
        element = self.driver.find_element(by_strategy, locator)
        element.clear()
        element.send_keys(value)

    def get_result(self):
        # <h1 style="bold; xcvdvf">result is 5000</h1>
        # return self.driver.find_element(By.XPATH, '//div').text  # "result is 5000"
        # return self.driver.find_element(By.XPATH, '//div').get_attribute('style')  # "bold; xcvdvf"
        return 1

    def is_hidden_visible(self):
        return self.is_visible("//*[text()=' This is the hidden message.']")

    def is_everything_visible(self):
        return self.is_visible("//h1[text()='Slide Down Toggle']") and self.is_visible('//label[@for="toggle"]')

    def is_visible(self, xpath):
        try:
            visible_element=self.driver.find_element(By.XPATH, xpath)
            print(xpath + " displayed: " + ( "True" if visible_element.is_displayed() else "False"))
            return visible_element.is_displayed()
        except NoSuchElementException:
            print('Exception occurred: ', str(traceback.format_exc()))
            return False

    def is_button_found(self):
        element_content='"Open"'
        js="""
        for(elem of document.querySelectorAll('*'))
            if(window.getComputedStyle(elem,':after').content === arguments[0])
                return true;
        return false;
        """
        return self.driver.execute_script(js, element_content)


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def page(driver):
    return Page(driver)


def test_tc001(driver: WebDriver, page: Page):
    page.visit_page()
    sleep(3)  # wait for load
    assert page.is_everything_visible()
    assert page.is_button_found()

    assert page.get_result() == 1
    sleep(3)  # see the result

def test_tc002(driver: WebDriver, page: Page):
    page.toggle()
    sleep(3)
    assert page.is_hidden_visible()
    page.toggle()
    sleep(3)
    assert page.is_everything_visible()
    assert page.is_button_found()
