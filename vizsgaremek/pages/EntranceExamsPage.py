import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By
from GenericPage import GenericPage
import config


class EntranceExamsPage(GenericPage):
    """
    EntranceExamsPage is a subclass of GenericPage,
    it handles the entrance exam page of Eduard software
    """

    url = config.BASE_URL + 'approveExamLocation.htm'

    mapping = {"table": (By.ID, "entranceExam"),
               "new_entrance_exam_button": (By.XPATH, '//*[@id="functions"]/a')
               }
    """
    Only these page elements are important for testing.
    """

    def go_to_new_entrance_exam(self):
        self.fill_form_with_value("new_entrance_exam_button")

    def get_table_data(self):
        """
        Gets and returns the entire entrance exam table as a list of dicts.
        :return: table data as list of dicts
        """
        return self.get_table_data_by_id(self.mapping['table'][1], True)
