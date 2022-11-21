import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By

from GenericPage import GenericPage
import config


class ProgramAdministrationPage(GenericPage):
    """
    This is the university program (e.g. Basic Medicine Course) modifier page in the Eduard system.
    """
    url = config.BASE_URL + 'modifySchool.htm'

    mapping = {"Neptun code": (By.ID, "program.neptunCode"),
               "save_button": (By.XPATH, '//*[@id="buttons"]/input')
               }
    """
    Only these page elements are important for testing.
    """

    def modify_neptun_code(self, neptun_code):
        """
        Modifies the neptun code of the selected program.
        :param neptun_code: new neptun code
        :return: None
        """
        self.fill_form_with_value("Neptun code", neptun_code)
        self.fill_form_with_value("save_button")
