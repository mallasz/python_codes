import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By
import re
import math

from GenericPage import GenericPage
import config


class ListAllStudentsPage(GenericPage):
    """
    ListAllStudentsPage is a subclass of GenericPage,
    it handles the student pagination page of Eduard software
    """
    url = config.BASE_URL + 'listAllStudents.htm'

    mapping = {"new_student_button": (By.XPATH, "//strong[text()='New student']/.."),
               "10": (By.XPATH, "//a[text()='10']"),
               "next": (By.XPATH, "//a[text()='Next page »']"),
               "prev": (By.XPATH, "//a[text()='« Previous page']"),
               "student": (By.ID, "student"),
               "page_number": (By.CLASS_NAME, "page")
               }
    """
    Only these page elements are important for testing.
    """

    def is_active_button(self, button_name):
        """
        Eduard's page uses an unusual solution to disable the previous and next page tags,
        instead of disabling or hiding, their href gets deleted.
        This method checks if an element is enabled, or disabled in this way.
        :param button_name: a name in the mapping (str)
        :return: bool, True if clickable
        """
        element = self.find_element(button_name)
        return element.get_attribute('href') != ''

    # these are links to go to other pages

    def go_to_new_student(self):
        self.fill_form_with_value("new_student_button")

    def press_next(self):
        self.fill_form_with_value("next")

    def press_prev(self):
        self.fill_form_with_value("prev")

    def get_student_table(self):
        """
        Gets and returns the table part on the page as a list of dicts.
        :return: table data as a list of dicts
        """
        table_data = self.get_table_data_by_id(self.find_element("student"), True)
        return table_data

    def get_number_of_students(self):
        """
        Gets the number of students from the label using regular expression.
        :return: number of students as int, None if not found
        """
        text_element = self.find_element('page_number')
        if res := re.match('^.* :: (?P<number>[0-9]+)$', text_element.text):
            return int(res['number'])
        return None

    def page_through_table(self):
        """
        Pagination and collecting the data from the students' tables.
        :return:
        """
        students_per_pages = 10
        self.fill_form_with_value(str(students_per_pages))  # clicks the "10" link/button
        num = self.get_number_of_students()  # number of students from the label
        page_num = math.ceil(num / students_per_pages)
        all_student_data = []  # collect data into this list
        for i in range(page_num):
            new_students = self.get_table_data_by_id("student", True)
            all_student_data += new_students
            if i < page_num - 1:  # there are more students on the next page, so go there
                assert len(new_students) == students_per_pages
                self.press_next()

        return all_student_data
