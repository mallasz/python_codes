import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *


def test_tc6(driver, login_page, start_page, user_page):
    """
    TC6 test case
    listing of users
    parameters are fixtures
    """
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # go to users' page
    start_page.go_to_users()
    # load current users into user_table
    user_table = user_page.get_user_table()

    # check if current (admin) user appears
    user_found = False
    for user in user_table:
        if user['USERNAME'] == 'admin':
            user_found = True
    assert user_found

    # log out and check if login page appears
    user_page.log_out()
    assert login_page.is_loaded_exactly()
