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
    URL = "http://selenium.oktwebs.training360.com/7904_potzarovizsga/rock_paper_scissors.html"
    game_rules = {
        "r": {"r": [0, 1, 0, 1], "p": [0, 0, 1, 1], "s": [1, 0, 0, 1]},
        "p": {"r": [1, 0, 0, 1], "p": [0, 1, 0, 1], "s": [0, 0, 1, 1]},
        "s": {"r": [0, 0, 1, 1], "p": [1, 0, 0, 1], "s": [0, 1, 0, 1]}
    }

    def get_wins_loses_dict(self, my_sign, opponents_sign):
        return self.game_rules[my_sign[0]][opponents_sign[0]]

    def get_wins_loses(self, my_sign, opponents_sign):
        values = {'r': 0, 'p': 1, 's': 2}
        # my_sign, opponents_sign = my_sign[0], opponents_sign[0]
        # if my_sign == opponents_sign:
        #     return [0, 1, 0, 1]
        idx = (values[opponents_sign[0]] - values[my_sign[0]] + 4) % 3
        result = [0, 0, 0, 1]
        result[idx] = 1
        return result

    def __init__(self, driver):
        self.driver = driver

    def visit_page(self):
        self.driver.get(self.URL)

    def fill_input(self, by_strategy, locator, value):
        element = self.driver.find_element(by_strategy, locator)
        element.clear()
        element.send_keys(value)

    def get_results(self):
        return [int(element.text) for element in
                self.driver.find_elements(By.XPATH, '//div[@class="scoreboard"]//span')]

    def click_on_sign(self, sign):
        self.driver.find_element(By.ID, sign).click()

    def get_opponent_sign(self):
        class_text = self.driver.find_element(By.XPATH, "//aside/div[1]/i[2]").get_attribute('class')
        if res := re.match('^fa fa-hand-(?P<opponent_sign>.*)-o$', class_text):
            return res['opponent_sign']
        return None


def add_lists(left, right):
    return [left[i] + right[i] for i in range(len(left))]
    # import numpy as np
    # return list(np.array(left)+np.array(right))


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


def test_rock_paper_scissors_tc1(driver, page):
    page.visit_page()
    sleep(3)  # wait for load

    assert page.get_results() == [0, 0, 0, 0]
    sleep(3)  # see the result


def test_rock_paper_scissors_tc2(driver, page):
    page.visit_page()
    sleep(3)  # wait for load

    page.click_on_sign("rock")

    opponent_sign = page.get_opponent_sign()

    if opponent_sign == "rock":
        assert page.get_results() == [0, 1, 0, 1]
        assert page.get_wins_loses("rock", opponent_sign) == [0, 1, 0, 1]
        print("rock")
    elif opponent_sign == "paper":
        assert page.get_results() == [0, 0, 1, 1]
        assert page.get_wins_loses("rock", opponent_sign) == [0, 0, 1, 1]
        print("paper")
    else:
        assert page.get_results() == [1, 0, 0, 1]
        assert page.get_wins_loses("rock", opponent_sign) == [1, 0, 0, 1]
        print("else")

    print(page.get_wins_loses("rock", opponent_sign))

    sleep(5)  # see the result


def test_rock_paper_scissors_tc3(driver, page):
    page.visit_page()
    sleep(3)  # wait for load

    status = [0] * 4

    for i in range(5):
        my_sign = random.choice(["rock", "paper", "scissors"])
        page.click_on_sign(my_sign)
        opponent_sign = page.get_opponent_sign()
        results = page.get_results()
        win_loose = page.get_wins_loses(my_sign, opponent_sign)
        status = add_lists(status, win_loose)
        assert results == status
        sleep(2)
    sleep(5)  # see the result
