import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *
import util


def test_tc10(driver, login_page, start_page,
              programs_page, program_administration_page, db):
    """
    TC10 test case
    modify a program in the Eduard software
    parameters are fixtures
    """
    program_name = "Basic Medicine Course"
    neptun_code = 'ALMA123'
    # reset the database to the default state to make sure the program to modify is there
    db.reset_database()
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # load program's page
    start_page.go_to_programs()
    # save the list of original programs
    original_programs = programs_page.get_table_data()
    # click on modify
    programs_page.go_to_modify(program_name)
    # set a new neptun code
    program_administration_page.modify_neptun_code(neptun_code)
    # save the modified list of programs
    modified_programs = programs_page.get_table_data()
    # there should be one difference, with the selected program name and new neptun code
    diff = util.list_diff(original_programs, modified_programs)
    assert len(diff) == 1
    modified_program = diff[0]
    assert modified_program['NAME'] == program_name
    assert modified_program['NEPTUN CODE'] == neptun_code

    # log out, it should be successful
    start_page.log_out()
    assert login_page.is_loaded_exactly()
