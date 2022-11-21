from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys


def check_if_todo_exists(s):
    """
    Checks if the todo having the given string exists
    :param s: string of the wanted item to check
    :return: bool
    """
    results = driver.find_elements(By.XPATH, f"//li[contains(.,' {s}')]")
    return len(results) > 0


def delete_todo(s):
    """
    Delete the given, existing item by finding and pressing its delete button
    :param s: string of the wanted item to remove
    :return: None
    """
    buttons = driver.find_elements(By.XPATH, f"//li[contains(.,' {s}')]/span/i")
    assert len(buttons) == 1
    buttons[0].click()


def add_new_todo(s):
    """
    Adds a new item with the needed string as todo text
    :param s: string of the wanted item to add
    :return: None
    """
    add_element = driver.find_element(By.XPATH, '//*[@id="container"]/input')
    add_element.send_keys(s)
    add_element.send_keys(Keys.ENTER)


def check_new_todo(s):
    """
    Tests new item creation with the string given as parameter
    :param s: str
    :return: None
    """
    assert check_if_todo_exists(s) is False
    add_new_todo(s)
    assert check_if_todo_exists(s) is True


def check_delete_todo(s):
    """
    Test item deletion by deleting the item with the given text
    :param s: str
    :return: None
    """
    assert check_if_todo_exists(s) is True
    delete_todo(s)
    time.sleep(2)  # Deletion is not immediate, waiting for animation to end
    assert check_if_todo_exists(s) is False


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://selenium.oktwebs.training360.com/probavizsga/todo.html")

    check_new_todo("Feed the cat")
    check_new_todo("Pet the cat")
    check_delete_todo("Pet the cat")
    check_delete_todo("Feed the cat")

    driver.close()
