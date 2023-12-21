import json
from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from urllib.parse import urlsplit, urlunsplit
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


#Function to input data into the table
def data_feed(driver,json_data):
    try:
        time.sleep(1)
        click_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//summary[contains(text( ), 'Table Data')]")))
        click_element.click()
        
    except TimeoutException:
        click_element = 'Not found'

    input_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID ,"jsondata")))
    input_element.send_keys(Keys.END)
    input_element.send_keys(Keys.CONTROL +"a") 
    input_element.send_keys(Keys.DELETE) 
    input_element.send_keys(json_data)

    refresh_button = driver.find_element(By.CLASS_NAME, "styled-click-button")
    refresh_button.click()


#Function to extract data from table
def extract_data(driver):
    table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "dynamictable")))
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]
    headers = [header.text.lower() for header in table.find_elements(By.TAG_NAME, "th")]
    extracted_data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = {headers[i]: cells[i].text for i in range(len(cells))}
        extracted_data.append(row_data)
    return extracted_data

def main(): 
    link = "https://testpages.herokuapp.com/styled/tag/dynamic-table.html"
    driver = Driver(uc=True)  
    driver.implicitly_wait(10)
    driver.get(link)

    data =[{"name" : "Bob", "age" : 20, "gender": "male"}, {"name": "George", "age" : 42, "gender": "male"}, {"name":
    "Sara", "age" : 42, "gender": "female"}, {"name": "Conor", "age" : 40, "gender": "male"}, {"name":
    "Jennifer", "age" : 42, "gender": "female"}]
    
    for person in data:
        person['age'] = str(person['age'])
    json_data = json.dumps(data)

    data_feed(driver,json_data)
    time.sleep(10)
    extracted_data = extract_data(driver)
    driver.quit()

    assert len(extracted_data) == len(data), "Number of rows in the table does not match the input data."
    for original, extracted in zip(data, extracted_data):
        assert original == extracted, f"Row data does not match: {original} != {extracted}"
        
    print("Assertion passed: Data in the table matches the input data.")


if __name__ == "__main__":
    main()
    print("success")



