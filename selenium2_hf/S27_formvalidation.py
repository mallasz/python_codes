from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.common.keys import Keys
import traceback


def fill_in(html_id, content=None):
    """
    fills the input field with the given content after clearing the filed
    if an empty field is necessary, clears it only
    :param html_id: the id of the target input field
    :param content: string to be filled in
    :return: the webelement object
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
    :param message_xpath: XPath of a webelement
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
        return expected_message == ''  # WebDriverWait() does not accept the empty string as visible, although it can be the expected result
    message_div = driver.find_element(By.XPATH, message_xpath)  # the webelement is found, and visible
    while time.time() <= start_time + max_timeout:  # wait until the maximal timeout time
        if message_div.text == expected_message:
            print("Found:", message_div.text)
            return True
        time.sleep(0.2)
    print("Different:", message_div.text)
    return False


# email validation check
EMAIL_MESSAGE_ID = 'test-email'
EMAIL_MESSAGE_XPATH = "//*[@id='test-email']/../../div[@class='validate-field-error-message']"


def check_email_test_focus():
    """
    click into the webelement, and after that in the "test-password" webelement to lose focus
    check the validation message
    :return: None
    """
    driver.find_element(By.ID, EMAIL_MESSAGE_ID).click()
    driver.find_element(By.ID, 'test-password').click()
    assert wait_for_message(EMAIL_MESSAGE_XPATH, 'Please enter an e-mail')


def check_email_test_not_mail():
    fill_in(EMAIL_MESSAGE_ID, 'cica')
    assert wait_for_message(EMAIL_MESSAGE_XPATH, 'Please check your E-Mail format')


def check_email_test_mail_but_wrong():
    fill_in(EMAIL_MESSAGE_ID, 'cica@cica.hu')
    assert wait_for_message(EMAIL_MESSAGE_XPATH, 'Checking login...')
    assert wait_for_message(EMAIL_MESSAGE_XPATH, 'Login does not exist')


def check_email_test_good():
    fill_in(EMAIL_MESSAGE_ID, 'yardy@yarr.com')
    assert wait_for_message(EMAIL_MESSAGE_XPATH, 'Checking login...')
    assert wait_for_message(EMAIL_MESSAGE_XPATH, '')


# test suites of the email field
def suite_email_field():
    check_email_test_focus()
    check_email_test_not_mail()
    check_email_test_mail_but_wrong()
    check_email_test_good()


# random message validation check
RANDOM_MESSAGE_ID = 'test-random-field'
RANDOM_MESSAGE_XPATH = "//*[@id='test-random-field']/../../div[@class='validate-field-error-message']"


def check_random_field_focus():
    driver.find_element(By.ID, RANDOM_MESSAGE_ID).click()
    driver.find_element(By.ID, 'test-password').click()
    assert wait_for_message(RANDOM_MESSAGE_XPATH, '')


def check_random_field_wrong_text():
    fill_in(RANDOM_MESSAGE_ID, 'cica')
    assert wait_for_message(RANDOM_MESSAGE_XPATH, 'Should contain "twelve"')


def check_random_field_empty_again():
    fill_in(RANDOM_MESSAGE_ID, '')
    assert wait_for_message(RANDOM_MESSAGE_XPATH, '')


def check_random_field_good():
    fill_in(RANDOM_MESSAGE_ID, '12cicatwelve12')
    assert wait_for_message(RANDOM_MESSAGE_XPATH, '')


# test suites of the random message field
def suite_random_field():
    check_random_field_focus()
    check_random_field_wrong_text()
    check_random_field_empty_again()
    check_random_field_good()


CARD_MESSAGE_ID = 'test-card-number'
CARD_MESSAGE_XPATH = "//*[@id='test-card-number']/../../div[@class='validate-field-error-message']"


# card number validation check
def check_card_focus():
    driver.find_element(By.ID, CARD_MESSAGE_ID).click()
    driver.find_element(By.ID, 'test-password').click()
    assert wait_for_message(CARD_MESSAGE_XPATH, 'Please enter a credit card number (no spaces)')


def check_card_wrong_number():
    fill_in(CARD_MESSAGE_ID, 'cica')
    assert wait_for_message(CARD_MESSAGE_XPATH, 'Please check your credit card nubmer')  # typo


def check_card_good():
    fill_in(CARD_MESSAGE_ID, '4111111111111111')
    assert wait_for_message(CARD_MESSAGE_XPATH, '')


# test suites of the card number field
def suite_card_field():
    check_card_focus()
    check_card_wrong_number()
    check_card_good()


driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/simplevalidation.html")

        suite_email_field()
        suite_random_field()
        suite_card_field()

    except Exception as e:
        print('Exception occurred: ', str(traceback.format_exc()))
    finally:
        if driver:
            driver.close()
