import sys
sys.path += ['../test_config', '../pages', '../test_utils']
import re
from selenium.webdriver.common.by import By

from GenericPage import GenericPage
import config


class StartPage(GenericPage):
    """
    This page appears after login.
    """

    url = config.BASE_URL + 'eduardStartPage.htm'

    mapping = {"student_page_button": (By.XPATH, "//a[@title='EDUard - Back to the main page!']"),
               "login_p": (By.ID, 'login'),
               "user_button": (By.XPATH, '//a[text()="Users"]'),
               "logout_button": (By.XPATH, '//a[text()="Log out"]'),
               "help_button": (By.XPATH, '//a[text()="Help"]'),
               "programs_button": (By.XPATH, '//a[text()="Programs"]'),
               "new_entrance_exam_button": (By.XPATH, '//a[text()="New Entrance Exam"]'),
               "entrance_exams_button": (By.XPATH, '//a[text()="Entrance exams"]'),
               }
    """
    Only these page elements are important for testing.
    """

    # these methods click on specific links or buttons
    def go_to_help(self):
        self.fill_form_with_value("help_button")

    def go_to_programs(self):
        self.fill_form_with_value("programs_button")

    def go_to_students(self):
        self.fill_form_with_value("student_page_button")

    def go_to_users(self):
        self.fill_form_with_value("user_button")

    def go_to_new_entrance_exam(self):
        self.fill_form_with_value("new_entrance_exam_button")

    def go_to_entrance_exams(self):
        self.fill_form_with_value("entrance_exams_button")

    def log_out(self):
        self.fill_form_with_value("logout_button")

    def get_user_and_role(self):
        """
        Logged-in user's details are written on the page. This method finds and extracts these.
        :return: a tuple with 2 strings, the first is the username, second is the role (e.g. Administrator)
        """
        login_text = self.find_element('login_p').text
        if res := re.match('Logged in: (?P<username>[^:]+)::(?P<role>[^: ]+) |', login_text):
            return res['username'], res['role']
        return None, None
