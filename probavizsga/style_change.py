from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time

# expected color codes for the tests before and after clicking the button, both for background and foreground
expected_background_colors_before_click = {"banner": "rgba(255, 255, 255, 1)", "button": "rgba(0, 132, 255, 1)"}
expected_colors_before_click = {"banner": "rgba(0, 0, 0, 1)", "button": "rgba(255, 255, 255, 1)"}
expected_background_colors_after_click = {"banner": "rgba(0, 132, 255, 1)", "button": "rgba(255, 255, 255, 1)"}
expected_colors_after_click = {"banner": "rgba(255, 255, 255, 1)", "button": "rgba(0, 0, 0, 1)"}

# expected class names
expected_classes = ["", "alt"]

# helper lists for easier handling
expected_background_colors = [expected_background_colors_before_click, expected_background_colors_after_click]
expected_colors = [expected_colors_before_click, expected_colors_after_click]

# we collect elements into this dict, indexed by element names
elements = {}


def check_colors(is_after):
    """
    Checks if class names, background colors and colors match the expected.
    This can be done both before and after clicking the button by indexing previously defined helper lists properly.
    :param is_after: 0 before clicking, 1 after clicking
    :return: None
    """
    class_name = elements["banner"].get_attribute("class")
    assert expected_classes[is_after] == class_name
    for element_name, element in elements.items():
        assert expected_background_colors[is_after][element_name] == element.value_of_css_property("background-color")
        assert expected_colors[is_after][element_name] == element.value_of_css_property("color")


def click_button():
    elements["button"].click()


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://selenium.oktwebs.training360.com/probavizsga/style_change.html")

    elements["banner"] = driver.find_element(By.ID, "banner-message")
    elements["button"] = driver.find_element(By.XPATH, '//div[@id="banner-message"]/button')

    check_colors(0)
    click_button()
    time.sleep(2)  # necessary for the animation to end
    check_colors(1)
    click_button()
    time.sleep(2)  # necessary for the animation to end
    check_colors(0)

    driver.close()
