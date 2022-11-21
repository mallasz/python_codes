from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.common.keys import Keys


def add_product(*content):
    """
    add new product to the product table
    :param content: any numbers of parameters
    :return: None
    """
    orig_row_number = count_rows()  # count the original rows
    add_button.click()
    for i, element in enumerate(driver.find_elements(By.XPATH,
                                                     "//div[@id='container']//table/tbody/tr[last()]/td/input[@type='text']")):
        element.clear()
        element.send_keys(content[i])  # put the contents in the target field
    assert orig_row_number + 1 == count_rows()  # check if the new row exists


def count_rows():
    """
    counts the rows of the table
    :return: number of rows
    """
    return len(driver.find_elements(By.XPATH, "//div[@id='container']//table/tbody/tr"))


def get_column_values(input_name):
    """
    :param input_name: determines the column of which values will return
    :return: list with the values of the column
    """
    return [str(element.get_attribute("value")) for element in driver.find_elements(By.NAME, input_name)]


def fill_search_field(search_text):
    """
    after clearing the field fills the search field with the given text
    if an empty field is necessary, clears it only
    :param search_text:
    :return:
    """
    search_field = driver.find_element(By.XPATH, "//input[@placeholder='Search...']")
    if search_text != '':
        search_field.clear()
        search_field.send_keys(search_text)
    else:
        # search_field.clear() doesn't call "onXXX" Javascript events, so a different clear method is needed
        driver.execute_script('document.getElementsByTagName("input")[0].select();')
        search_field.send_keys(Keys.BACKSPACE)


def search_check(search_text):
    """
    check, if the search works
    :param search_text:
    :return: None
    """
    fill_search_field("")  # set the search field empty
    original = get_column_values('name')  # collects product names
    fill_search_field(search_text)
    filtered = get_column_values('name')  # collects the filtered product names
    res = [s for s in original if
           search_text in s]  # res is a list of product names that has the search text as a substring
    assert res == filtered  # compared the results


def delete(category):
    """
    deletes products having the given category
    :param category:
    :return: None
    """
    original = get_column_values('category')  # collects product categories
    # collect delete buttons, where the category is equivalent to the given category
    delete_buttons = driver.find_elements(By.XPATH, f"//table//tr/td[4]/input[@value='{category}']/../../td[5]/input")
    [element.click() for element in delete_buttons]  # click the delete buttons
    after_delete = get_column_values('category')  # collects product categories again
    for category_type in after_delete:
        assert category_type != category  # check if the category which should be deleted is deleted
    assert len(original) == len(after_delete) + len(delete_buttons)  # check if nothing else was deleted


driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/editable-table.html")

        add_button = driver.find_element(By.XPATH, "//button[contains(.,'Add')]")

        # add new products
        add_product("Samsung", 200, 13, "Electronics")
        add_product("Iphone", 100, 10, "Electronics")

        # check the search field
        search_check("")
        search_check("Iphone")
        search_check("ball")
        search_check("yxcvb")

        # delete a product category
        fill_search_field("")
        delete("Electronics")

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
