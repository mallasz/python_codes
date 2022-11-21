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


class Page:
    URL = " http://selenium.oktwebs.training360.com/7904_potzarovizsga/geometry.html"

    def __init__(self, driver):
        self.driver = driver

    def visit_page(self):
        self.driver.get(self.URL)

    def fill_inputs(self, a, m):
        self.fill_input(By.ID,"a",a)
        self.fill_input(By.ID, "m",m)

    def fill_input(self, by_strategy, locator, value):
        element = self.driver.find_element(by_strategy, locator)
        element.clear()
        element.send_keys(value)

    def click_button_triangle(self):
        self.driver.find_element(By.ID,"submitT").click()

    def click_button_rhombus(self):
        self.driver.find_element(By.ID, "submitD").click()

    def get_input_values(self):
        a=self.driver.find_element(By.ID,'a').get_attribute('value')
        m=self.driver.find_element(By.ID,'m').get_attribute('value')
        return(a,m)

    def get_span(self, html_id):
        try:
            span = self.driver.find_element(By.ID, html_id)
            return span.text
        except NoSuchElementException:
            return None

    def get_result(self):
        return self.get_span("resultT"), self.get_span("resultD")


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


def test_tc1(driver, page):
    page.visit_page()
    sleep(3)  # wait for load

    assert page.get_input_values() == ('', '')
    assert page.get_result() == ('', '')
    sleep(3)  # see the result

def test_tc2(driver, page):
    page.visit_page()
    sleep(3)  # wait for load
    page.fill_inputs(5,4)
    page.click_button_triangle()
    assert page.get_result() == ('10.00', '')
    sleep(3)  # see the result

def test_tc3(driver, page):
    page.visit_page()
    sleep(3)  # wait for load
    page.fill_inputs(7,5)
    page.click_button_triangle()
    page.click_button_rhombus()
    assert page.get_result() == ('17.50', '35')
    sleep(3)  # see the result
