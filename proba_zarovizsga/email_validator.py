from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.keys import Keys
import traceback


def fill_in(html_id, content=None):
    """
    fills the input field with the given content after clearing the filed
    if an empty field is necessary, clears it only
    :param html_id: the id of the target input field
    :param content: string to be filled in
    :return: the WebElement object
    """
    element = driver.find_element(By.ID, html_id)
    element.click()
    if content:
        element.clear()
        element.send_keys(content)
    else:
        # search_field.clear() doesn't call "onXXX" Javascript events, so a different clear method is needed
        driver.execute_script(f'document.getElementById("{html_id}").select();')
        element.send_keys(Keys.BACKSPACE)
    return element


def wait_for_message(message_xpath, expected_message, max_timeout=5):
    """
    Wait until the field given by XPath is displayed, and its content is the expected message
    If it happens the return value is True, else False
    :param message_xpath: XPath of a WebElement
    :param expected_message: string that is expected
    :param max_timeout: maximal time we want to wait
    :return: Bool
    """
    print("Looking for:", expected_message)
    start_time = time.time()  # start time of the function, the next timeout is counting from here
    try:
        message_element = WebDriverWait(driver, max_timeout).until(
            EC.visibility_of_element_located((By.XPATH, message_xpath)))  # wait until the element is visible
        if message_element.text == expected_message:
            print("Found:", message_element.text)
            return True
    except TimeoutException as te:
        print("Not found:", message_xpath)
        # WebDriverWait() does not accept the empty string as visible, although it can be the expected result
        return expected_message == ''
    message_div = driver.find_element(By.XPATH, message_xpath)  # the WebElement is found, and visible
    while time.time() <= start_time + max_timeout:  # wait until the maximal timeout time
        if message_div.text == expected_message:
            print("Found:", message_div.text)
            return True
        time.sleep(0.2)
    print("Different:", message_div.text)
    return False


# email validation check
EMAIL_MESSAGE_ID = 'email'
MESSAGE_XPATH = '//div[@class="validation-error"]'
SUBMIT_ID = 'submit'


def click_on_submit():
    driver.find_element(By.ID, SUBMIT_ID).click()


def check_email_test_not_mail():
    fill_in(EMAIL_MESSAGE_ID)
    click_on_submit()
    assert wait_for_message(MESSAGE_XPATH, 'Kérjük, töltse ki ezt a mezőt.')


def check_email_test_mail_but_wrong(invalid_email):
    fill_in(EMAIL_MESSAGE_ID, invalid_email)
    click_on_submit()
    assert wait_for_message(MESSAGE_XPATH,
                            f'Kérjük, adja meg a „@” utáni részt is. A(z) „{invalid_email}” cím nem teljes.')


def check_email_test_good(valid_email):
    fill_in(EMAIL_MESSAGE_ID, valid_email)
    click_on_submit()
    assert wait_for_message(MESSAGE_XPATH, '')


driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/sl10_proba_zarovizsga/email_validator.html")

        # empty e-mail field
        check_email_test_not_mail()
        # invalid e-mail address
        check_email_test_mail_but_wrong("teszt@")
        # valid e-mail
        check_email_test_good("teszt@elek.hu")

    except Exception as e:
        print('Exception occurred: ', str(traceback.format_exc()))
    finally:
        if driver:
            driver.close()
