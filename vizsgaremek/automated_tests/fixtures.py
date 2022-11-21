import sys
sys.path += ['../test_config', '../pages', '../test_utils']
import pytest
import util
from DB import DB

from LoginPage import LoginPage
from StartPage import StartPage
from ListAllStudentsPage import ListAllStudentsPage
from NewStudentPage import NewStudentPage
from UserPage import UserPage
from NewUserPage import NewUserPage
from EntranceExamAdministrationPage import EntranceExamAdministrationPage
from EntranceExamsPage import EntranceExamsPage
from ProgramsPage import ProgramsPage
from ProgramAdministrationPage import ProgramAdministrationPage

"""
This module creates fixtures for testing.
This is a pytest fixture collection.
"""


@pytest.fixture
def db():
    """
    Creates and returns a new database connector
    :return: DB
    """
    return DB()


@pytest.fixture()
def driver():
    """
    Creates and returns a new Selenium webdriver.
    After the caller quits, yield gets back here, and the driver (and the browser window) quits.
    :return: the driver
    """
    driver = None
    try:
        driver = util.get_driver()
        yield driver
    finally:
        if driver:
            driver.quit()


# these are different page objects for different tests

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def start_page(driver):
    return StartPage(driver)


@pytest.fixture
def entrance_exam_administration_page(driver):
    return EntranceExamAdministrationPage(driver)


@pytest.fixture
def entrance_exams_page(driver):
    return EntranceExamsPage(driver)


@pytest.fixture
def programs_page(driver):
    return ProgramsPage(driver)


@pytest.fixture
def program_administration_page(driver):
    return ProgramAdministrationPage(driver)


@pytest.fixture
def user_page(driver):
    return UserPage(driver)


@pytest.fixture
def list_all_students_page(driver):
    return ListAllStudentsPage(driver)


@pytest.fixture
def new_student_page(driver):
    return NewStudentPage(driver)


@pytest.fixture
def new_user_page(driver):
    return NewUserPage(driver)
