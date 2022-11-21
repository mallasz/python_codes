from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import traceback


def count_movies():
    return len(driver.find_elements(By.XPATH, '//div[@class="container-movies"]'))


mapping = {"register_button": (By.XPATH, '//button[text()="Register"]'),
           "film_title": (By.ID, 'nomeFilme'),
           "release_year": (By.ID, 'anoLancamentoFilme'),
           "chronological_year_of_events": (By.ID, 'anoCronologiaFilme'),
           "trailer_url": (By.ID, 'linkTrailerFilme'),
           "image_url": (By.ID, 'linkImagemFilme'),
           "film_summary_url": (By.ID, 'linkImdbFilme'),
           "save_button": (By.XPATH, '//button[text()="Save"]'),
           "order_select": (By.ID, 'ordenarFilmes')
           }
"""
Giving a name to a strategy-locator tuple to easily map 
dict keys to input fields of a form.
e.g.: "film_title": (By.ID, 'nomeFilme')
"""

new_movie_data = {
    "film_title": "Black widow",
    "release_year": 2021,
    "chronological_year_of_events": 2020,
    "trailer_url": "https://www.youtube.com/watch?v=Fp9pNPdNwjI",
    "image_url": "https://m.media-amazon.com/images/I/914MHuDfMSL._AC_UY327_FMwebp_QL65_.jpg",
    "film_summary_url": "https://www.imdb.com/title/tt3480822/"
}


def fill_form(data=None):
    """
    Takes a dict of name: value mapping, and fills everything.
    :param data: A dict of name-value pairs.
    :return: None
    """
    if data is None:
        data = {}
    for name, value in data.items():
        fill_form_with_value(name, value)


def fill_form_with_value(name, value=None):
    """
    Takes a form input's name and desired value, and fills it in.
    :param name: A name in the mapping dict for this webpage.
    :param value: A value.
    :return: None
    """
    if name not in mapping:
        raise KeyError(f"Mapping has no {name} in it")
    strategy, locator = mapping[name]
    fill(strategy, locator, value)


def fill(strategy, locator, value=None):
    """
    Fills any html input element given by a descriptor and value.
    First we find the element, determine element type, then convert the value, and fill it in.
    :param locator: anything that describes the element,
    :param value: fills this value if there is any
    :param strategy: defaults to By.ID, gives a way to interpret the element_descriptor
    :return: None
    """
    element = driver.find_element(strategy, locator)  # Try to locate the element

    # Check if the element is a select, find the appropriate option by visible text.
    # Only visible text is supported at the moment.
    if element.tag_name == "select":
        Select(element).select_by_visible_text(value)
        return

    # Buttons are also a valid target for fill function, just click on them.
    elif element.tag_name == "button":
        element.click()
        return

    # In this condition branch it can only be an input tag.
    elif element.tag_name == "input":
        # Input fields have many types, it's important to check it.
        input_type = element.get_attribute('type')

        # Text is the most common type.
        if input_type in ['text', "number"]:
            element.clear()  # First clear the field, and if any value is given as a parameter, fill it in.
            if value:
                element.send_keys(str(value))
            return


def count_ordering_options():
    return len(driver.find_elements(By.XPATH, "//select[@id='ordenarFilmes']/option"))


def get_movies():
    return [element.get_attribute('innerText').split("\n") for element in
            driver.find_elements(By.XPATH, '//div[@class="container-movies"]/h2')]


driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/sl10_proba_zarovizsga/film_register.html")
        time.sleep(5)  # website has lots of animations, sleeps are required

        # test movies number
        assert count_movies() == 24

        # test sorting
        assert count_ordering_options() == 3

        # register a new movie
        fill_form_with_value("register_button")
        time.sleep(3)
        fill_form(new_movie_data)
        time.sleep(3)
        fill_form_with_value("save_button")
        time.sleep(5)
        assert count_movies() == 25
        movie_titles = [movie[0] for movie in get_movies()]
        assert new_movie_data["film_title"] in movie_titles

    except Exception as e:
        print('Exception occurred: ', str(traceback.format_exc()))
    finally:
        if driver:
            driver.close()
