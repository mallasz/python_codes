import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *


def test_tc7(driver, login_page, start_page, list_all_students_page):
    """
    TC7 test case
    students listing by pagination
    parameters are fixtures
    """
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # load student page
    start_page.go_to_students()
    # collect all students' data
    all_students = list_all_students_page.page_through_table()

    # read student number from the label, it should match the number of students collected
    num = list_all_students_page.get_number_of_students()
    assert num == len(all_students)

    # log out, it should be successful
    start_page.log_out()
    assert login_page.is_loaded_exactly()
