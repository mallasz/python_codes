# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def calculate():
    """
    :return: Tuple with 2 parameters: the calculated result as a String, and the result on the page as a String
    """
    expression = driver.find_element(By.TAG_NAME, "form").text.split("\n")[0].strip(
        " =?")  # the mathematical expression on the page
    driver.find_element(By.ID, 'submit').click()  # submit button click
    result_on_page = driver.find_element(By.ID, 'result').text
    result = eval(expression)  # the calculated result
    return str(result), str(result_on_page)


def load_page():
    driver.get(base_url)


base_url = "http://selenium.oktwebs.training360.com/7709_zarovizsga/matek_app.html"

driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        load_page()

        # TC1
        expression = driver.find_element(By.TAG_NAME, "form").text.split("\n")[0]
        submit_button = driver.find_element(By.ID, 'submit')
        assert expression[-1] == "?"
        assert driver.find_element(By.ID, 'result').text == ""
        assert submit_button.is_enabled() and submit_button.is_displayed()

        # TC2
        load_page()
        submit_button = driver.find_element(By.ID, 'submit')
        submit_button.click()
        res = driver.find_element(By.ID, 'result').text

        for i in range(3):
            submit_button.click()
            assert res == driver.find_element(By.ID, 'result').text

        # TC3
        for i in range(10):
            load_page()
            result, result_on_page = calculate()
            assert result == result_on_page

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
