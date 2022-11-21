import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *
import util


def test_tc12(driver, login_page, start_page, programs_page):
    """
    TC12 test case
    save Eduard's programs into a CSV file
    parameters are fixtures
    """
    # file name to write
    file_name = 'programs.csv'
    # column names
    columns = ['ABBREVIATION', 'NAME', 'NEPTUN CODE']
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # go to program page
    start_page.go_to_programs()
    # get table data for later comparison
    programs = programs_page.get_table_data()
    # export data to file
    programs_page.export_table(file_name, columns)
    # load saved CSV
    programs_csv = util.get_csv_data(file_name)
    # exported data should match with the data on the page
    assert len(programs_csv) == len(programs)  # check same length
    for csv, program in zip(programs_csv, programs):
        for column in columns:
            assert csv[column] == program[column]  # check same data

    # log out and check for success
    start_page.log_out()
    assert login_page.is_loaded_exactly()
