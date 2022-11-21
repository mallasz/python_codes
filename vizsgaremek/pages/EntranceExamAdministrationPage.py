import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By
from GenericPage import GenericPage
import config


class EntranceExamAdministrationPage(GenericPage):
    """
    EntranceExamAdministrationPage is a subclass of GenericPage,
    it handles the entrance exam administration page of Eduard software
    where a new entrance exam can be registered.
    """

    url = config.BASE_URL + 'inputExamLocation.htm'

    mapping = {"Country": (By.ID, "entranceExam.country"),
               "City/Town": (By.ID, 'entranceExam.town'),
               "street/number": (By.ID, 'entranceExam.streetAndNumber'),
               "Number of students": (By.ID, 'entranceExam.numberOfStudents'),
               "Exam date": (By.ID, 'examDate'),
               "committee": (By.ID, 'entranceExam.committee'),
               "Representative": (By.ID, 'entranceExam.proposedBy'),
               "save_button": (By.XPATH, '//*[@id="buttons"]/input'),
               }
    """
    Only these page elements are important for testing.
    """

    def new_entrance_exam(self, data_dict):
        """
        Fills in the form and submits to create a new entrance exam.
        :param data_dict: dict with new entrance exam parameters
        :return: None
        """
        self.fill_form(data_dict)
        self.fill_form({"save_button": None})
