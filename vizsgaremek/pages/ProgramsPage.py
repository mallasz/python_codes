import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By

import util
from GenericPage import GenericPage
import config


class ProgramsPage(GenericPage):
    """
    List of programs page
    """

    url = config.BASE_URL + 'listSchools.htm'

    mapping = {"table": (By.ID, "program")
               }
    """
    Only these page elements are important for testing.
    """

    def go_to_modify(self, name):
        """
        Finds and clicks the modify button of the chosen program
        :param name: name of the program
        :return: None
        """
        modify_button = self.driver.find_element(By.XPATH,
                                                 f"//table[@id='program']//tr/td[text()='{name}']/../td[last()]/a[2]")
        modify_button.click()

    def get_table_data(self):
        """
        Gets and returns the program table.
        :return: None
        """
        return self.get_table_data_by_id(self.mapping['table'][1], True)

    def export_table(self, file_name, columns=None):
        """
        Gets and saves the program table as a CSV.
        If columns parameter is set, only the chosen columns are exported, in the selected order.
        :param file_name: file name as str
        :param columns: list of strings, the column names
        :return: None
        """
        if columns is None:
            columns = []
        data = self.get_table_data()
        util.write_csv_data(file_name, data, columns)
