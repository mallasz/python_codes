# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


def load_page():
    driver.get(base_url)


def get_page_info():
    """
    collects the current status of the game, and returns fields as a dictionary
    the dictionary has 5 items:
        money as a string,
        bet as a string
        result is the result's text as a string,
        and win and lose as bool, whether those elements are visible
    :return:
    """
    money_element = driver.find_element(By.ID, 'cash')
    bet_element = driver.find_element(By.ID, 'bet')
    result_element = driver.find_element(By.ID, 'outcome')
    win_element = driver.find_element(By.ID, 'youwin')
    lose_element = driver.find_element(By.ID, 'youlose')
    return {'money': money_element.get_attribute('value'), 'bet': bet_element.get_attribute(
        'value'), 'result': result_element.text, 'win': (win_element.get_attribute(
        'style') == ''), 'lose': (lose_element.get_attribute('style') == '')}


def click_button(html_id):
    button_element = driver.find_element(By.ID, html_id)
    button_element.click()


def bet_amount(amount):
    """
    fills the bet input field
    :param amount: the given amount
    :return: None
    """
    bet_element = driver.find_element(By.ID, 'bet')
    bet_element.clear()
    bet_element.send_keys(str(amount))


# TC_000
def original_values_test_tc000():
    """
    test before filling the fields
    :return: None
    """
    load_page()
    original_values = get_page_info()
    # print(original_values)
    assert original_values['money'] == '100'
    assert original_values['bet'] == ''
    assert original_values['result'] == '-'


# TC_001
def first_flip_test_tc001():
    """
    tests with the given parameters, clicks on tails button,
    and checks if losing the coin flip the result is heads and the amount of money is 90
    and checks if winning the coin flip the result is tails and the amount of money is 110
    :return: None
    """
    load_page()
    bet_amount(10)
    click_button('tails')
    result_values = get_page_info()
    # print(result_values)
    if result_values['win']:
        # print('We won 10')
        assert result_values['result'] == 'tails'
        assert result_values['money'] == '110'
    else:
        # print('We lost 10')
        assert result_values['result'] == 'heads'
        assert result_values['money'] == '90'


base_url = "http://selenium.oktwebs.training360.com/r2d2_felezovizsga/coin_flip.html"
driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        original_values_test_tc000()
        first_flip_test_tc001()


    except Exception as e:
        print('Exception occured: ', e)

    finally:
        if driver:
            driver.close()
