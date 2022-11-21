import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *
import util


def test_tc11(driver, login_page, start_page, user_page, db):
    """
    TC11 test case
    delete a user
    parameters are fixtures
    """
    # reset the database to the default state to make sure the user to delete is there
    db.reset_database()
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # go to user page
    start_page.go_to_users()
    # save the original user table data
    users = user_page.get_user_table()
    # delete the last user
    user_to_be_deleted = users[-1]
    user_name = user_to_be_deleted['USERNAME']
    user_page.delete_user(user_name)
    # save the modified user table data
    new_users = user_page.get_user_table()
    # there should be 1 difference, deleted user should not exist on the page
    diff = util.list_diff(new_users, users)
    assert len(diff) == 1
    assert diff[0]['USERNAME'] == user_name
    # DB has logical deletion, there should be no active user with the given username
    statement = "SELECT COUNT(*) FROM eduard_user WHERE activeUser = 1 and username = %s"
    assert db.get_data(statement, (user_name, ))[0][0] == 0

    # log out and check for success
    start_page.log_out()
    assert login_page.is_loaded_exactly()
