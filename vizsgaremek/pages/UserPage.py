import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By
import re

from GenericPage import GenericPage
import config


class UserPage(GenericPage):
    """
    Eduard's users' lists page
    """
    url = config.BASE_URL + 'listUsers.htm'

    mapping = {"login_p": (By.ID, 'login'),
               "logout_button": (By.XPATH, '//a[text()="Log out"]'),
               "new_user_button": (By.XPATH, '//div[@id="functions"]/a'),
               "label": (By.XPATH, '//span[@class="pagebanner"]')
               }
    """
    Only these page elements are important for testing.
    """

    def log_out(self):
        self.fill_form_with_value("logout_button")

    def go_to_new_users(self):
        self.fill_form_with_value("new_user_button")

    def get_user_table(self):
        """
        Gets the user table's data
        :return: data as list of dicts
        """
        data = self.get_table_data_by_id("user", True)
        return data

    def delete_user(self, user_name):
        """
        Delete a user by clicking its delete button and accept the alert.
        :param user_name: user name as str
        :return: None
        """
        delete_button = self.driver.find_element(By.XPATH,
                                                 f"//table[@id='user']//tr/td[text()='{user_name}']/../td[last()]/a[1]")
        delete_button.click()
        alert = self.driver.switch_to.alert
        alert.accept()

    def get_number_of_users(self):
        """
        Gets the number of users from the label using regular expression.
        :return: number of users as int, None if not found
        """
        text_element = self.find_element('label')
        if res := re.match('^(?P<number>[0-9]+) .*', text_element.text):
            return int(res['number'])
        return None
