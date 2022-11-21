from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from datetime import date, time


def issue_ticket():
    """
    click the issue ticket button
    :return: None
    """
    driver.find_element(By.ID, "issue-ticket").click()


def set_name_input(name):
    """
    set the passenger input field
    :param name: the name of the passenger
    :return: None
    """
    passenger = driver.find_element(By.ID, "passenger")
    passenger.clear()
    passenger.send_keys(name)


def get_name():
    """
    Get the passenger's name on the ticket
    :return: Str
    """
    return driver.find_element(By.ID, "passenger-name").text


def get_date():
    """
    get the dates from the ticket, and the ticket stub
    :return: Str
    """
    departure_date_text = driver.find_element(By.ID, "departure-date-text").text
    side_departure_date = driver.find_element(By.ID, "side-detparture-date").text
    assert departure_date_text == side_departure_date
    return departure_date_text


def get_time():
    """
    get the times from the ticket, and the ticket stub
    :return: Str
    """
    departure_time_text = driver.find_element(By.ID, "departure-time-text").text
    side_departure_time = driver.find_element(By.ID, "side-departure-time").text
    assert departure_time_text == side_departure_time
    return departure_time_text


def set_invalid_date(invalid_date):
    """
    set an invalid date in the date filed
    :param invalid_date:
    :return:
    """
    wrong_date = driver.find_element(By.ID, "departure-date")
    wrong_date.send_keys(invalid_date)
    wrong_date.send_keys("\t" + Keys.DELETE + "\t" + Keys.DELETE + "\n")


def set_date_input(input_id, dt):
    """
    :param input_id: id of an HTML filed
    :param dt: date, datetime or time object to be put in the field
    :return: None
    """
    date_input = driver.find_element(By.ID, input_id)  # search the input field
    date_input_type = date_input.get_attribute('type')  # get the input filed type attribute
    date_string = ''  # date_string will be the formatted string, which would be put in the field
    if date_input_type == 'date':
        date_string = dt.strftime("%Y-%m-%d")
    elif date_input_type == 'time':
        date_string = dt.strftime('%H:%M:%S.%f')[:-3]
    else:
        raise ValueError(f'Invalid input type: "{date_input_type}"')
    # js code sets the value of the input fields, independent of regional settings
    js_code = f'document.getElementById("{input_id}").value="{date_string}";'
    driver.execute_script(js_code)


# dictionary contains languages and matching accept_languages
lang_dict = {'hu': 'hu,hu_HU', 'en': 'en,en_US', 'es': 'es,es_ES', 'de': 'de,de_DE',
             'ms': 'ms,ms_MY', 'ja': 'ja-JP', 'zh': 'zh,zh_CN', 'th': 'th_TH', 'fi': 'fi_FI', 'ar': 'ar_EG'}


def set_locale(lang):
    """
    set the language of the browser
    :param lang:
    :return:
    """
    global options
    if lang in lang_dict:
        options.add_experimental_option('prefs', {'intl.accept_languages': lang_dict[lang]})
    options.add_argument(f'--lang={lang}')


def load_the_page():
    driver.get("http://selenium.oktwebs.training360.com/sl10_proba_zarovizsga/hogwarts.html")


driver = None
if __name__ == '__main__':
    try:
        options = webdriver.ChromeOptions()
        set_locale('hu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        load_the_page()

        # completely fill in
        set_name_input("Harry Potter")
        set_date_input("departure-date", date(2022, 9, 1))
        set_date_input("departure-time", time(10, 0, 0))
        issue_ticket()

        assert get_name() == 'HARRY POTTER'
        assert get_date() == '2022-09-01'
        assert get_time() == '10:00AM'

        # partially fill in
        set_name_input("")
        set_date_input("departure-date", date(2022, 9, 1))
        set_date_input("departure-time", time(10, 0, 0))
        issue_ticket()

        assert get_name() == ''
        assert get_date() == '2022-09-01'
        assert get_time() == '10:00AM'

        # incomplete fill in
        load_the_page()  # simple clear does not clear the last valid set date
        set_name_input("Harry Potter")
        set_invalid_date("2022")
        set_date_input("departure-time", time(10, 0, 0))
        issue_ticket()

        assert get_name() != 'HARRY POTTER'
        assert get_date() != '2022'
        assert get_time() != '10:00AM'

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
