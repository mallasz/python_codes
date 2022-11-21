import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By

from GenericPage import GenericPage
import config


class LoginPage(GenericPage):
    """
    LoginPage is a subclass of GenericPage, it handles the login page of Eduard software
    """

    url = config.BASE_URL + 'login.htm'  # running currently on localhost

    mapping = {"username": (By.ID, "username"),
               "password": (By.XPATH, '//input[@type="password"]'),
               "submit": (By.XPATH, '//input[@type="submit"]')}
    """
    Only these page elements are important for testing.
    """

    passwords = {"admin": "admin12",
                 "superMHSC": "super12",
                 "superCAHS": "super12",
                 "cahsAdmin": "admin12",
                 "caaesAdmin": "admin12",
                 "invalid_user": "1234567890",
                 "": "",
                 "Test_admin": "Test12"  # This is my test user
                 }
    """
    Passwords of some pre-defined users. This way the documentation is not necessary for testing.
    """

    def login(self, username, password=None):
        """
        Pairs the username with the password according to the password map and logs in.
        :param username: username as a parameter (str)
        :param password: optional parameter to override password in passwords dict
        :return:
        """
        if password is None:
            password = self.passwords[username]
        self.go_there()
        self.fill_form({"username": username,
                        "password": password})
        self.fill_form({"submit": None})
