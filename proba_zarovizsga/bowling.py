from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def press_button(num):
    if num == 0:
        num = "Gutter"
    driver.find_element(By.XPATH, f"//button[@type='button'][text()='{num}']").click()


def get_markers():
    return [element.text for element in driver.find_elements(By.XPATH, "//td[starts-with(@id,'marker')]")]


def get_frames():
    return [element.text for element in driver.find_elements(By.XPATH, "//td[starts-with(@id,'frame')]")]


def list_to_str(lst):
    return [str(x) for x in lst]


def get_comment():
    return driver.find_element(By.ID, 'comments').text


def load_the_page():
    driver.get("http://selenium.oktwebs.training360.com/sl10_proba_zarovizsga/bowling-scorecard.html")


driver = None
if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        load_the_page()

        # before game
        markers = get_markers()
        frames = get_frames()
        assert markers == [''] * 10
        assert frames == [''] * 10

        # 11 strikes
        for i in range(11):
            press_button(10)
        markers = get_markers()
        assert markers == list_to_str([10, 20, 40, 60, 80, 100, 120, 140, 160, 200])

        # invalid roll
        load_the_page()
        assert get_comment() == ''
        press_button(6)
        press_button(5)
        assert get_comment() == 'Invalid Roll - there are only ten pins!'

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
