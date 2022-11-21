from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class GenericPage:
    """
    GenericPage class for filling and clicking any WebElements of a general form or page.
    It's completely independent of any specific system being tested.
    """

    mapping = {}
    """
    Giving a name to a strategy-locator tuple to easily map 
    the column names (header) of a CSV file to input fields of a form.
    e.g.: "username": (By.ID, "username")
    """

    url = ""
    """
    URL of the page to be tested.
    """

    def __init__(self, driver, url=None):
        """
        Constructor.
        :param driver: a Selenium driver object to use
        :param url: (optional) override the default URL
        """
        self.driver = driver
        if url:
            self.url = url

    def is_loaded_exactly(self):
        """
        Returns whether the driver's current_url matches the stored url.
        :return: bool
        """
        return self.driver.current_url == self.url

    def is_loaded(self):
        """
        Returns whether the driver's current_url (partially) matches the stored url.
        Get parameters can alter the URL so a prefix match can be useful.
        :return: bool
        """
        return self.driver.current_url.startswith(self.url)

    def find_element(self, name):
        """
        Similar method to Selenium's find_element, but this uses the mapping's name.
        :param name: a key from self.mapping
        :return: a WebElement
        """
        strategy, locator = self.mapping[name]
        return self.driver.find_element(strategy, locator)

    def find_elements(self, name):
        """
        Similar method to Selenium's find_elements, but this uses the mapping's name.
        :param name: a key from self.mapping
        :return: a WebElement
        """
        strategy, locator = self.mapping[name]
        return self.driver.find_elements(strategy, locator)

    def wait_for_load(self, max_timeout=5):
        """
        Wait for complete loading of a page.
        The url must match, and all the pre-defined elements given by the mapping dict must exist.
        :param max_timeout: maximum waiting time in seconds
        :return: bool, True on success
        """
        start_time = time.time()
        while not self.is_loaded() and max_timeout >= (time.time() - start_time):
            time.sleep(0.2)
        if time.time() >= max_timeout + start_time:
            return False

        try:
            for by_strategy, locator in self.mapping.values():
                timeout = max_timeout - (time.time() - start_time)
                WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by_strategy, locator)))
        except TimeoutException:
            return False
        return True

    def go_there(self, wait=True):
        """
        Load the stored url, and possibly wait for complete load.
        :param wait: True if a complete load is necessary.
        When mapping has an element defined, that is not present, setting this to True is not recommended.
        :return: None
        """
        self.driver.get(self.url)
        if wait:
            self.wait_for_load()

    def get_table_data_by_id(self, table_id, get_dict=False):
        """
        Gets table data as a list of lists, or if "get_dict" parameter is true, then as a list of dictionaries.
        The keys of the dictionaries are the header names of the table.
        :param table_id: id of the table to load
        :param get_dict: type needed
        :return: the table data as list of lists or list of dicts
        """
        res = []
        if get_dict:  # dict format
            header = [th.text for th in self.driver.find_elements(By.XPATH, f"//table[@id='{table_id}']//th")]
            for row in self.get_table_data_by_id(table_id, False):  # recursively call in list mode
                res.append({k: v for k, v in zip(header, row)})
        else:  # list format
            # first determine the number of non-header rows
            for row_index, row_element in enumerate(  # row_element is not used
                    self.driver.find_elements(By.XPATH, f"//table[@id='{table_id}']//tr/td/.."), start=1):
                # make an xpath to get all tds of the nth non-header row
                row_tds = self.driver.find_elements(By.XPATH, f"//table[@id='{table_id}']//tr[{row_index}]//td")
                res.append([td.text for td in row_tds])
        return res

    def fill_form(self, data=None):
        """
        Takes a dict of name: value mapping, and fills everything.
        :param data: A dict of name-value pairs.
        :return: None
        """
        if data is None:
            data = {}
        for name, value in data.items():
            self.fill_form_with_value(name, value)

    def fill_form_with_value(self, name, value=None):
        """
        Takes a form input's name and desired value, and fills it in.
        :param name: A name in the mapping dict for this webpage.
        :param value: A value.
        :return: None
        """
        if name not in self.mapping:
            raise KeyError(f"Mapping has no {name} in it")
        strategy, locator = self.mapping[name]
        self.fill(strategy, locator, value)

    def fill(self, strategy, locator, value=None):
        """
        Fills any html input element given by a descriptor and value.
        First we find the element, determine element type, then convert the value, and fill it in.
        :param locator: anything that describes the element,
        :param value: fills this value if there is any
        :param strategy: defaults to By.ID, gives a way to interpret the element_descriptor
        :return: None
        """
        element = self.driver.find_element(strategy, locator)  # Try to locate the element

        # First try to check if this is a radio button. This is only supported by name now.
        if strategy == By.NAME:
            # Check if we got a radio button. At this time this is only possible by name.
            elements = self.driver.find_elements(strategy, locator)
            if len(elements) > 0:
                element = elements[0]
                # If the tag_name is 'input', and the type is 'radio', it's a radio button.
                if element.tag_name == 'input' and element.get_attribute('type') == 'radio':
                    # Construct an xpath that only finds the element in question with value as its value.
                    xpath = f"//input[@type='radio'][@name='{locator}'][@value='{value}']"
                    self.driver.find_element(By.XPATH, xpath).click()
                    return

        # Check if the element is a select, find the appropriate option by visible text.
        # Only visible text is supported at the moment.
        if element.tag_name == "select":
            Select(element).select_by_visible_text(value)
            return

        # Submit buttons, normal buttons and links are also a valid target for fill function, just click on them.
        # Submit buttons can be made using a separate submit tag, or adding submit type to an input tag.
        # Buttons work the same with the button tag or <input type="button">
        elif element.tag_name in ["submit", "button", "a"]:
            element.click()
            return

        # In this condition branch it can only be an input tag.
        elif element.tag_name == "input":
            # Input fields have many types, it's important to check it.
            input_type = element.get_attribute('type')

            # Text is the most common type. Empty type also defaults to text.
            # Password fields' only difference is hiding their values.
            if input_type in ['text', '', 'password', None, "number"]:
                element.clear()  # First clear the field, and if any value is given as a parameter, fill it in.
                if value:
                    element.send_keys(str(value))
                return

            # Checkboxes can be checked by default, only click on them if the needed value is different.
            elif input_type == 'checkbox':
                checked = element.get_attribute('checked')
                to_be_checked = value in ['True', 'true', True, 1, '1']
                if checked != to_be_checked:
                    element.click()
                return

            # This is the other kind of button/submit type.
            elif input_type in ['button', 'submit']:
                element.click()
                return

            # There are many date-like types, convert the value (a datetime or similar type) into the correct format.
            date_string = None
            if input_type == 'date':
                date_string = value.strftime("%Y-%m-%d")
            elif input_type == 'datetime-local':
                date_string = value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
            elif input_type == 'month':
                date_string = value.strftime('%Y-%m')
            elif input_type == 'week':
                date_string = f"{value.year}-W{value.isocalendar().week:02d}"
            elif input_type == 'time':
                date_string = value.strftime('%H:%M:%S.%f')[:-3]
            if date_string is not None:
                # Send it to the browser using JavaScript. This works regardless of locale settings.
                self.driver.execute_script('arguments[0].value=arguments[1]', element, date_string)
                return
