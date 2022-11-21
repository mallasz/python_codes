# imports
import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver


class Page:
    """
    Using the Page Object Model, this is the Page side. Test cases are using this object from the outside
    """

    URL = "http://selenium.oktwebs.training360.com/5201_kepesitovizsga/twitter.html"
    """
    URL of the page to load and test
    """

    def __init__(self, driver: WebDriver):
        """
        A simple constructor
        :param driver: a WebDriver object to use
        """
        self.driver = driver

    def visit_page(self):
        """
        Load the page
        :return: None
        """
        self.driver.get(self.URL)

    def send_tweet(self, text):
        """
        Send a tweet on the tested page
        :param text: text of the tweet
        :return: None
        """
        textarea = self.driver.find_element(By.TAG_NAME, 'textarea')
        textarea.clear()
        textarea.send_keys(str(text))
        self.driver.find_element(By.XPATH, "//button[text()='Tweet']").click()

    def get_list_of_x_text(self, x_text):
        """
        Get the text of something shown on page. That something is identified by its x-text attribute
        :param x_text: x-text attribute of the elements
        :return: the result as a list of strings
        """
        return [element.text for element in self.driver.find_elements(By.XPATH, f"//*[@x-text='{x_text}']")]

    def get_tweet_user_names(self):
        """
        Get the user names associated with the tweets shown on page.
        :return: user names as a list of strings
        """
        return self.get_list_of_x_text('tweet.name')

    def get_tweet_texts(self):
        """
        Get the tweet texts shown on page.
        :return: tweets as a list of strings
        """
        return self.get_list_of_x_text('tweet.tweet')

    def get_who_to_follow_names(self):
        """
        Get the tweet texts shown on page.
        :return: tweets as a list of strings
        """
        return self.get_list_of_x_text('generateAvatarFromName(followersSuggestion.name)')

    def get_who_to_unfollow_names(self):
        """
        Get the tweet texts shown on page.
        :return: tweets as a list of strings
        """
        return self.get_list_of_x_text('generateAvatarFromName(following.name)')

    def follow_nth_user(self, n):
        """
        Press the n-th follow button. The exact number could be determined by user names.
        :param n: index of the button, starting with 0
        :return: None
        """
        self.press_nth_button_with_text(n, 'Follow')

    def unfollow_nth_user(self, n):
        """
        Press the n-th unfollow button. The exact number could be determined by user names.
        :param n: index of the button, starting with 0
        :return: None
        """
        self.press_nth_button_with_text(n, 'Unfollow')

    def press_nth_button_with_text(self, n, text):
        buttons = self.driver.find_elements(By.XPATH, f"//button[text()='{text}']")
        buttons[n].click()

    def follow_user(self, user_name):
        """
        Follow the chosen user.
        :param user_name: user to follow
        :return: None
        """
        user_list = self.get_who_to_follow_names()
        idx = user_list.index(user_name)
        self.follow_nth_user(idx)

    def unfollow_user(self, user_name):
        """
        Unfollow the chosen user.
        :param user_name: user to unfollow
        :return: None
        """
        user_list = self.get_who_to_unfollow_names()
        idx = user_list.index(user_name)
        self.unfollow_nth_user(idx)


@pytest.fixture()
def driver():
    """
    Creates and returns a new Selenium webdriver.
    After the caller quits, yield gets back here, and the driver (and the browser window) quits.
    :return: the driver
    """
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        yield driver
    finally:
        if driver:
            driver.close()


@pytest.fixture()
def page(driver):
    """
    A fixture to create and return a Page object
    :param driver:
    :return: Page
    """
    return Page(driver)


# posting a new tweet, and check if it appeared
def test_twitter_tc001(driver: WebDriver, page: Page):
    new_tweet_text = "What's happening: New twitter post arrived"  # tweet text to send
    page.visit_page()  # load page
    sleep(1)  # wait for load

    page.send_tweet(new_tweet_text)  # create new tweet with the given content
    texts = page.get_tweet_texts()  # get tweets
    assert new_tweet_text in texts  # check if it's there

    sleep(2)  # see the result


# Follow user CN and check if it was successful
def test_twitter_tc002(driver: WebDriver, page: Page):
    user_to_test = "CN"  # user to test
    page.visit_page()
    sleep(1)  # wait for load

    following = page.get_who_to_unfollow_names()  # get the current list of follows
    assert user_to_test not in following  # check if the user is not followed

    page.follow_user(user_to_test)  # follow
    sleep(2)

    following = page.get_who_to_unfollow_names()  # get the current list of follows
    assert user_to_test in following  # check if the user is followed

    sleep(2)  # see the result


# unfollow PN
def test_twitter_tc003(driver: WebDriver, page: Page):
    user_to_test = "PN"  # user to test
    page.visit_page()
    sleep(1)  # wait for load

    suggestions = page.get_who_to_follow_names()  # get the current list of suggestions
    assert user_to_test not in suggestions  # user should not be there

    page.unfollow_user(user_to_test)  # unfollow
    sleep(2)

    suggestions = page.get_who_to_follow_names()  # get the current list of suggestions
    assert user_to_test in suggestions  # user should be there

    sleep(2)  # see the result
