from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = None
if __name__ == '__main__':
    try:

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://selenium.oktwebs.training360.com/sl10_proba_zarovizsga/periodic_table.html")
        # read file line by line
        rows = []
        try:
            with open("data.txt", "r") as f:
                for line in f:
                    # add data to the rows list, index 0 is periodic element number, index 1 is its name
                    rows.append(line.split(", "))
        except FileNotFoundError as e:
            print("File not found: " + e.filename)

        # read web elements, lis is the list of li webelements (contains periodic element number)
        # spans (contains periodic element names) are matching spans
        lis = driver.find_elements(By.XPATH, '//li[@data-pos]')
        spans = driver.find_elements(By.XPATH, '//li[@data-pos]/span')
        for index, (span, li) in enumerate(zip(spans, lis)):
            # compare the element numbers and names in order to the numbers and names read from file
            assert rows[index][0].strip() == li.get_attribute("data-pos")
            assert rows[index][1].strip() == span.text.strip()

    except Exception as e:
        print('Exception occurred: ', e)
    finally:
        if driver:
            driver.close()
