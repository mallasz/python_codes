# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def load_page():
    driver.get(base_url)


def get_message():
    """
    :return: String, the text of the message id
    """
    validation_message = driver.find_element(By.ID, 'message').text
    return validation_message


def fill(html_id, value):
    """
    finds an element by an id, and fill with the value
    :param html_id:
    :param value:
    :return: None
    """
    element = driver.find_element(By.ID, html_id)
    element.clear()
    element.send_keys(value)


def fill_user_pass(username, password):
    """
    fills the username and the password fields with the given data
    :param username:
    :param password:
    :return: None
    """
    fill('usrname', username)
    fill('psw', password)


def get_check(html_id):
    """
    checks if the element class attribute is equal to "valid"
    :param html_id:
    :return: Bool
    """
    element = driver.find_element(By.ID, html_id)
    return element.get_attribute('class') == 'valid'


def get_checks():
    """
    :return: Tuple with 4 parameters which are False or True
    """
    return get_check('letter'), get_check('capital'), get_check('number'), get_check('length')


base_url = "http://selenium.oktwebs.training360.com/7709_zarovizsga/pw_field.html"
driver = None

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        load_page()

        # TC_001
        fill_user_pass('admin', 'aB12aB12')
        checks = get_checks()
        assert checks == (True, True, True, True)

        # TC_002
        fill_user_pass('admin', 'asdfghjk')
        checks = get_checks()
        assert checks == (True, False, False, True)

        # TC_003
        fill_user_pass('admin', 'ASDFGHJK')
        checks = get_checks()
        assert checks == (False, True, False, True)

        # TC_004
        fill_user_pass('admin', '12345678')
        checks = get_checks()
        assert checks == (False, False, True, True)

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
