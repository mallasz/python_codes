import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *


def test_tc13(driver, login_page, start_page):
    """
    TC13 test case
    admin logout
    parameters are fixtures
    """
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # check if login was successful and the page is loaded
    assert start_page.is_loaded_exactly()
    # log out
    start_page.log_out()
    # check if logout was successful
    assert login_page.is_loaded_exactly()
    # try to load start page by setting the url
    start_page.go_there(False)
    # this should not be possible with a logged-out user
    assert not start_page.is_loaded()
