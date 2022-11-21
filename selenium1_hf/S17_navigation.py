from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
import requests


def check_redirect(url):
    """
    using the requests module gets the information whether it is a redirected url
    :param url:
    :return: bool
    """
    try:
        res = requests.get(url)
        return len(res.history) > 0 and 300 <= res.history[0].status_code < 400
    except requests.exceptions:
        return False


def set_attribute(element, name, value):
    """
    uses JavaScript to modify an element's attribute
    :param element: WebElement to modify
    :param name: attribute's name
    :param value: attribute's value
    :return: None
    """
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", element, name, value)


def opens_new_window(link):
    """
    checks if the given link would open in a new window
    :param link:
    :return: bool
    """
    return link.get_attribute("target") == "_blank"


driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/general.html")

        link_num = 0  # link_num is the index of the link
        while link_num < len(links := driver.find_elements(By.XPATH, '//a[@href]')):
            """until all the links are done,
            links get invalid after clicking on a link, they need to be re-parsed"""
            link = links[link_num]  # current link to click
            if opens_new_window(link):
                set_attribute(link, 'target', '')
                """ if it wants to open a new window, is modified to stay on the current one"""
            href = link.get_attribute("href")  # getting the link's url
            link.click()
            referrer = driver.execute_script('return window.document.referrer')  # getting the referrer with JavaScript
            print('-' * 100)
            print(f'Jelenlegi url: {driver.current_url}')
            print(f'Betöltendő url: {href}')
            print(f'Referrer: {referrer}')
            if driver.current_url == href:
                print("Egyező url-ek")
            elif check_redirect(href):
                print("Átirányítás miatt nem egyeznek az url-ek")
            else:
                print("Nem egyező url-ek")
            driver.back()
            link_num += 1

    except Exception as e:
        print('Exception occured: ', e)

    finally:
        if driver:
            driver.close()
