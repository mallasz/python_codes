import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *
import util


exam_data = {
    "Country": "Hungary",
    "City/Town": "Budapest",
    "Number of students": 20,
    "Exam date": "2023-12-31",
    "Representative": "Agent, Bob"
}
"""
data of the new exam which should be registered
"""


def test_tc8(driver, login_page, start_page,
             entrance_exams_page, entrance_exam_administration_page, db):
    """
    TC8 test case
    new entrance exam registration
    parameters are fixtures
    """
    # reset the database to the default state to make sure the data of the new entrance exam is not in the database
    db.reset_database()
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # go to entrance exam page
    start_page.go_to_entrance_exams()
    # read existing exams
    original_table = entrance_exams_page.get_table_data()
    # go to new exam registration page
    start_page.go_to_new_entrance_exam()
    # add a new exam
    entrance_exam_administration_page.new_entrance_exam(exam_data)
    # read modified list
    modified_table = entrance_exams_page.get_table_data()
    # there should be exactly 1 new entry, with the entered data
    diff = util.list_diff(original_table, modified_table)
    assert len(diff) == 1
    new_exam_data = diff[0]
    assert new_exam_data['AGENT'] == exam_data['Representative']
    assert new_exam_data['NUMBER OF STUDENTS'] == str(exam_data['Number of students'])
    address_and_date = f"{exam_data['City/Town']}, {exam_data['Country']}, {exam_data['Exam date']}"
    assert new_exam_data['ADDRESS AND DATE'] == address_and_date

    # log out and check if login page appears
    start_page.log_out()
    assert login_page.is_loaded_exactly()
