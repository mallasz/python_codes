from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, date, time

'''
Formats expected by the browser
-date "%Y-%m-%d"
-datetime text
-datetime-local yyyy-MM-ddThh:mm:ss.SSS
-month The format is "yyyy-MM" where yyyy is year in four or more digits, and MM is 01-12.
-week "yyyy-Www" where yyyy is year in four or more digits, and ww is 01-53.
-time The format is "HH:mm", "HH:mm:ss" or "HH:mm:ss.SSS" where HH is 00-23, mm is 00-59, ss is 00-59, and SSS is 000-999.
'''


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
    elif date_input_type == 'datetime' or date_input_type == 'text':  # datetime is an invalid type, get text instead
        date_string = dt.strftime('%Y.%m.%d %H:%M:%S:%f')[:-3]
    elif date_input_type == 'datetime-local':
        date_string = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    elif date_input_type == 'month':
        date_string = dt.strftime('%Y-%m')
    elif date_input_type == 'week':
        date_string = f"{dt.year}-W{dt.isocalendar().week:02d}"
    elif date_input_type == 'time':
        date_string = dt.strftime('%H:%M:%S.%f')[:-3]
    else:
        raise ValueError(f'Invalid input type: "{date_input_type}"')
    # js code sets the value of the input fields, independent from regional settings
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


driver = None
options = webdriver.ChromeOptions()
if __name__ == '__main__':
    try:
        options = webdriver.ChromeOptions()
        set_locale('en')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("http://selenium.oktwebs.training360.com/forms.html")

        set_date_input("example-input-date", date(2021, 6, 5))
        set_date_input("example-input-date-time",
                       datetime(2012, 5, 5, 5, 5, 5, 555000))  # this is invalid, Chrome recognises this as text
        set_date_input("example-input-date-time-local", datetime(2000, 5, 12, 12, 1))
        set_date_input("example-input-month", date(1995, 12, 1))
        set_date_input("example-input-week", date(2015, 12, 25))
        set_date_input("example-input-time", time(0, 25, 0))

        sleep(5)

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
