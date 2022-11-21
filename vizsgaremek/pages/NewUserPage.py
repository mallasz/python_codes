import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By

from GenericPage import GenericPage
import config


class NewUserPage(GenericPage):
    """
    Page for adding new users
    """
    url = config.BASE_URL + 'addUser.htm'

    mapping = {"logout_button": (By.XPATH, '//a[text()="Log out"]'),
               "save_button": (By.XPATH, '//input[@type="submit"]'),

               "username": (By.NAME, 'user.username'),
               "password": (By.NAME, 'password'),
               "password2": (By.NAME, 'repeatPassword'),
               "family_name": (By.NAME, 'user.name.familyName'),
               "given_name": (By.NAME, 'user.name.givenName'),
               "e-mail": (By.NAME, 'user.notificationEmail'),
               "role": (By.ID, 'user.role')
               }
    """
    Only these page elements are important for testing.
    """

    def log_out(self):
        self.fill_form_with_value("logout_button")

    def add_user(self, data=None):
        """
        Adds a new user to the system
        :param data: dict for new user details
        :return: None
        """
        if data is None:
            data = {}
        self.fill_form(data)
        self.fill_form_with_value('save_button')
