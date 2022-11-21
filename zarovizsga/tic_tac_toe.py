# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import random
from selenium.common.exceptions import NoAlertPresentException


def load_page():
    driver.get(base_url)


def get_all_fields():
    """
    :return: List of elements which class are "tile"
    """
    return driver.find_elements(By.XPATH, '//div[@class="tile"]')


def get_all_field_texts():
    """
    :return: List with texts of the fields
    """
    return [field.text for field in get_all_fields()]


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


def click_start():
    driver.find_element(By.XPATH, '//div[@class="settings"]/button').click()


def get_board_size():
    return int(driver.find_element(By.ID, 'board-size').get_attribute('value'))


def get_win_size():
    return int(driver.find_element(By.ID, 'win-size').get_attribute('value'))


def set_board(board_size, win_size):
    """
    Sets the board size and the win size and click
    :param board_size:
    :param win_size:
    :return: None
    """
    fill('board-size', board_size)
    fill('win-size', win_size)
    click_start()


def check_and_accept_alert():
    """
    Clicks and accepts the alert box, and returns with its text
    :return: String or None if not found
    """
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text
    except NoAlertPresentException:  # if alert is not found
        return None


def put_mark(fields, my_board_size, row, column):
    """
    Clicks on that field
    :param fields: list of fields
    :param my_board_size: board size
    :param row: row of the chosen field
    :param column: column of the chosen field
    :return: None
    """
    index = (row - 1) * my_board_size + (column - 1)
    fields[index].click()


base_url = "http://selenium.oktwebs.training360.com/7709_zarovizsga/tic_tac_toe.html"

driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # TC_001
        load_page()
        default_board_size = get_board_size()
        field_texts = get_all_field_texts()
        assert field_texts == ['?'] * (default_board_size * default_board_size)

        for i in range(10):  # check it in a reasonable amount of numbers
            board_size = random.randint(3, 49)
            win_size = random.randint(board_size + 1, 50)
            set_board(board_size, win_size)
            alert_text = check_and_accept_alert()
            assert alert_text == 'Make your params consistant !'  # typo in text

        # TC_002
        load_page()  # reload with default sizes
        board_size = get_board_size()
        win_size = get_win_size()
        fields = get_all_fields()

        # put marks with both player in the first and second line, stop before the first player wins
        for i in range(win_size - 1):
            put_mark(fields, board_size, 1, i + 1)
            put_mark(fields, board_size, 2, i + 1)
        put_mark(fields, board_size, 1, win_size)  # put mark with the first payer to win
        sleep(2)  # alert doesn't appear immediately
        alert_text = check_and_accept_alert()
        assert alert_text == 'Game Over, player 1wins'

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
