import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from selenium.webdriver.common.by import By

import util
from GenericPage import GenericPage
import config


class NewStudentPage(GenericPage):
    """
    Pages for adding new students. There are many subpages for the same function,
    because the mandatory input elements are distributed along more forms.
    This class handles all of them.
    """

    url = 'http://localhost:8084/newStudent.htm'

    mapping = {
        # these are on the first page
        "Family name": (By.NAME, "student.name.familyName"),
        "Given name": (By.NAME, "student.name.givenName"),
        "Sex": (By.NAME, "student.sex"),
        "Mother's maiden name": (By.NAME, "student.motherMaidenName"),
        "Date of birth": (By.ID, "dateOfBirth"),
        "City/town": (By.NAME, "student.birthplaceTown"),
        "Nationality": (By.ID, "student.nationality"),

        # these are on the third page
        "Applied to": (By.ID, "student.application.appliedToProgram"),
        "Main program": (By.ID, "selectMainProgram"),
        "Academic year": (By.ID, "academicYear"),

        # these are present at most
        "save_data": (By.NAME, "submitButton"),
        "next_button": (By.XPATH, '//div[@class="nScreen"]/a[@title="Következő képernyő"]')
    }
    """
    Only these page elements are important for testing.
    """

    first_page_inputs = ["Family name", "Given name", "Sex", "Mother's maiden name",
                         "Date of birth", "City/town", "Nationality"]

    third_page_inputs = ["Applied to", "Main program", "Academic year"]

    def fill_in_student_data(self, data=None):
        """
        This method creates a new student.
        First fill in the input fields on the first page, then save, click on the next button twice.
        Then fill the third page, and save.
        :param data: new student's data as a dict
        :return: None
        """
        if data is None:
            data = {}
        self.fill_form(util.filter_dict(data, self.first_page_inputs))
        self.fill_form_with_value("save_data")
        self.fill_form_with_value("next_button")
        self.fill_form_with_value("next_button")
        self.fill_form(util.filter_dict(data, self.third_page_inputs))
        self.fill_form_with_value("save_data")

    def create_students_from_csv(self, file_name):
        """
        Reads the students' data from a CSV file and create them.
        :param file_name: CSV file name
        :return: number of students read
        """
        csv_data = util.get_csv_data(file_name)
        for student in csv_data:
            student['Sex'] = student['Sex'][0]
            self.fill_in_student_data(student)
            self.go_there(False)
        return len(csv_data)
