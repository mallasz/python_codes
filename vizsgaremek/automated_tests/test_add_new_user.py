import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By
from fixtures import *
import util


# this is the test data for the new user
new_user_data = {
    "username": "Test_admin",
    "password": "Test12",
    "password2": "Test12",
    "family_name": "Test",
    "given_name": "Administrator",
    "e-mail": "",
    "role": "ADMIN"
}


def test_tc3(driver, login_page, start_page, user_page, new_user_page, db):
    """
    TC3 test case
    Add new user
    parameters are fixtures
    """
    db.reset_database()  # reset database to the default state

    # load login page, and log in as admin
    login_page.go_there()
    login_page.login('admin')

    # go to users page and store current users
    start_page.go_to_users()
    user_table_old = user_page.get_user_table()

    # go to new user page and add a new user, then come back and store current users again
    user_page.go_to_new_users()
    new_user_page.add_user(new_user_data)
    user_page.go_there()
    user_table_new = user_page.get_user_table()
    new_user_number = user_page.get_number_of_users()

    # compare the number of users in the label and in the table
    assert len(user_table_new) == new_user_number

    # Compare the old and the new list of users. There should be exactly 1 new user with the parameters entered.
    diff = util.list_diff(user_table_old, user_table_new)
    assert len(diff) == 1
    user_data = diff[0]
    assert user_data['USERNAME'] == new_user_data['username']
    assert user_data['NAME'] == new_user_data['family_name'] + ', ' + new_user_data['given_name']
    assert user_data['USER ROLE'] == new_user_data['role']

    # log out of the system
    start_page.go_to_users()
    start_page.log_out()

    # try to log in with the new user
    login_page.go_there()
    login_page.login(new_user_data['username'])

    # login should be successful, and username should match the new user
    assert start_page.is_loaded_exactly()
    user, role = start_page.get_user_and_role()
    assert user == new_user_data['username']
    assert role == 'Administrator'

    # log out and check if it was successful
    start_page.log_out()
    assert login_page.is_loaded_exactly()

    # check if the new user is in the database with the given parameters
    db_result = db.get_data('SELECT username, familyName, givenName FROM eduard_user WHERE username=%s',
                            (new_user_data['username'],))

    assert len(db_result) == 1
    assert db_result[0][0] == new_user_data['username']
    assert db_result[0][1] == new_user_data['family_name']
    assert db_result[0][2] == new_user_data['given_name']


def test_tc4(driver, login_page, start_page, user_page, new_user_page, db):
    """
    TC4 test case
    Add new user with empty data fields
    parameters are fixtures
    """

    def check_validation(input_name, error_message):
        """
        Search for validator message and compare with the reference message.
        :param input_name: input field's name, this is different from the error tag
        :param error_message: error text
        :return: bool, True if they match
        """
        error_element = driver.find_element(By.XPATH,
                                            f"//input[@name='{input_name}']/preceding-sibling::div[1][@id='error']")
        return error_message == error_element.text

    # login as admin, list users, and go to new users page
    login_page.go_there()
    login_page.login('admin')
    start_page.go_to_users()
    user_table_old = user_page.get_user_table()
    user_page.go_to_new_users()

    # count users in the database, this might be a different number from rows in the webpage due to logical deletion
    count_before = int(db.get_data('SELECT count(*) FROM eduard_user')[0][0])

    # add an empty user
    new_user_page.add_user({})

    # count after the attempt to add new user
    count_after = int(db.get_data('SELECT count(*) FROM eduard_user')[0][0])
    # these should be equal
    assert count_before == count_after

    # validation messages should appear and be these texts
    assert check_validation("user.username", "Username required")
    assert check_validation("password", "Password must be given")
    assert check_validation("user.name.familyName", "Family name required")
    assert check_validation("user.name.givenName", "Given name required")

    # go back to user list and read again
    user_page.go_there()
    user_table_new = user_page.get_user_table()
    # there should be no difference
    diff = util.list_diff(user_table_old, user_table_new)
    assert len(diff) == 0
    # log out
    start_page.log_out()
    assert login_page.is_loaded_exactly()
