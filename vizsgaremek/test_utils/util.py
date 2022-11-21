from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import logging

"""
Global utility functions that are useful and used different places.
"""


def get_driver(headless=False):
    """
    Creates a chrome driver and returns it
    :param headless: set it to True to run Chrome in the background (runs somewhat faster)
    :return: a Selenium driver
    """
    logging.getLogger('WDM').setLevel(logging.ERROR)

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def filter_dict(d, list_of_keys):
    """
    Returns a filtered dict that only contains keys present in the list_of_keys parameter.
    This is useful when another function returns a dict with data not needed,
    or when a dictionary's data is sent to different subpages.
    :param d: a dict
    :param list_of_keys: a list of needed keys
    :return: dict
    """
    return {k: v for (k, v) in d.items() if k in list_of_keys}


def get_csv_data(file_name):
    """
    Reads a CSV's header and data into a list of dicts. Dict keys are header column names.
    :param file_name: CSV file name
    :return: list of dicts
    """
    res = []
    with open(file_name, 'r', encoding='utf-8', newline='') as f:
        csv_file = csv.reader(f)
        header = next(csv_file)
        for row in csv_file:
            res.append({k: v for k, v in zip(header, row)})
    return res


def write_csv_data(file_name, data=None, header=None):
    """
    Writes a CSV file with the given file name, data, and column names.
    :param file_name: file name
    :param data: a list of dicts
    :param header: (optional) A list of strings with column names.
    The CSV will have these columns in this order. If it's missing, the data's first row's keys will be used.
    :return: None
    """
    if data is None:
        data = []
    if header is None and len(data) > 0:
        header = data[0].keys()
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        csv_file = csv.writer(f)
        if header:
            csv_file.writerow(header)
            for row in data:
                csv_file.writerow([row[key] for key in header])


def list_diff(smaller_list, extended_list):
    """
    Gives the difference between two lists.
    This is used to compare two tables, before and after adding a new value to check if the system works.
    Only lists the values present in new_list and not in old_list.
    For deletion testing, use the parameters in reverse order.
    :param smaller_list: old, smaller list
    :param extended_list: new, extended list
    :return: list of the different values
    """
    return [d for d in extended_list if d not in smaller_list]
