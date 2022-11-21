import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By

from fixtures import *


def test_tc1(driver, login_page, start_page):
    """
    TC1 test case
    admin login
    parameters are fixtures
    """
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # start page should be loaded if it was successful
    assert start_page.is_loaded_exactly()
    # read username and role, it should be admin and Administrator
    user, role = start_page.get_user_and_role()
    assert user == 'admin'
    assert role == 'Administrator'
    # log out and check if login page is loaded
    start_page.log_out()
    assert login_page.is_loaded_exactly()


def test_tc2(driver, login_page):
    """
    TC2 test case
    admin login
    parameters are fixtures
    """
    # load login page
    login_page.go_there()
    # try to log in with empty username and password field
    login_page.login('')
    # system should not take this as a valid login
    # check the validator message text and url
    assert driver.current_url == 'http://localhost:8084/login.htm?login_error=1'
    divs = driver.find_elements(By.XPATH, "//div[@class='errormessage']")
    assert len(divs) == 1 and divs[0].text == 'Login failed!'
