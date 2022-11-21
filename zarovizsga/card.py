# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def load_page():
    driver.get(base_url)


def draw_a_card():
    driver.find_element(By.ID, 'submit').click()


def analyze_card(s):
    """
    get the text of the card as a parameter and returns with its suit and rank and with the card text
    :param s:
    :return: Tuple of 3 strings: suit, rank, card_text
    """
    card_text = s
    suit = card_text[-1]  # clubs (♣), diamonds (♦), hearts (♥) or spades (♠)
    rank = card_text[:-1]  # number between 2-10 or A, K, Q, J
    return suit, rank, card_text


def get_last_card():
    """
    :return: with the last card analyzed text (suit, rank, card_text)
    """
    card_text = driver.find_element(By.ID, 'lastResult').text
    return analyze_card(card_text)


def get_history():
    """
    :return: with the history as list of analyzed texts (suit, rank, card_text)
    """
    cards = driver.find_elements(By.XPATH, '//ul[@id="deck"]/div[@class="card"]')
    return [analyze_card(card.text) for card in cards]


base_url = "http://selenium.oktwebs.training360.com/7709_zarovizsga/card.html"

driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # TC_001
        load_page()
        for i in range(10):
            draw_a_card()
        last_card = get_last_card()
        last_card_in_history = get_history()[-1]
        assert last_card[2] == last_card_in_history[2]

        # TC_002
        load_page()
        for i in range(40):
            draw_a_card()
        cards_in_history = get_history()
        number_of_spades = len([card[2] for card in cards_in_history if card[0] == '♠'])
        assert 9 <= number_of_spades <= 11

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
