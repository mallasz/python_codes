import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *


def test_tc5(driver, login_page, start_page):
    """
    TC5 test case
    open and close help
    parameters are fixtures
    """
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')

    # help opens in a new tab, so save the current window handle
    main_window = driver.window_handles[0]
    # open help tab
    start_page.go_to_help()
    # switch to help tab
    help_window = driver.window_handles[1]
    driver.switch_to.window(help_window)

    # check if this is a new tab, and help url is loaded
    assert main_window != help_window
    assert driver.current_url == 'http://localhost:8084/adminHelp.htm'
    # close tab and switch back
    driver.close()
    driver.switch_to.window(main_window)

    # start page should appear a screen, then after logout, login screen should load
    assert start_page.is_loaded_exactly()
    start_page.log_out()
    assert login_page.is_loaded_exactly()
