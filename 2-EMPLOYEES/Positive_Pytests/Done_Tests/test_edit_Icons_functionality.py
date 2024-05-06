import random
import time
import pytest
from faker import Faker
from selenium.webdriver.chrome import ChromeDriverManager, webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

faker = Faker()


def delay():
    time.sleep(random.randint(1, 2))  # Delay all actions from 1 to 2 sec


# ===========================================================
# Optional:
def entries_per_page_number(chrome_driver):
    # Optional: Find the number of Entries per page
    try:
        setEntriesNumber = WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, ":re:")))
        # Read the number of entries per page in the combobox:
        entriesPerPage = setEntriesNumber.get_attribute("value")
        print("\nThe number of entries per page is up to:", entriesPerPage)
    except TimeoutException:
        print("\nEntries number is not visible.")


def all_records_display(chrome_driver):
    # Loop through the pages:
    page_number = 1
    recordNumber = 1
    while True:
        record_xpath = f"(//span[contains(., 'edit')])[{recordNumber}]"

        # Process all records on the page:
        try:
            # Wait for the "Edit" icon to be present:
            edit_icon = WebDriverWait(chrome_driver, 5).until(EC.presence_of_element_located((By.XPATH, record_xpath)))
            # Click on the "Edit" icon:
            chrome_driver.execute_script("arguments[0].click();", edit_icon)

            delay()

            try:
                # Verify the form title == "Employee Info"
                title = chrome_driver.find_element(By.XPATH, "//h3[contains(.,'Employee Info')]")
                # Read the First name
                fNameBox = chrome_driver.find_element(By.XPATH, "//input[@name='firstName']")
                firstName = fNameBox.get_attribute("value")
                # Read the Last name
                lNameBox = chrome_driver.find_element(By.XPATH, "//input[@name='lastName']")
                lastName = lNameBox.get_attribute("value")

                print(f"{title.text}:  {firstName} {lastName}")
            except NoSuchElementException:
                print("The form 'Employee Info' is NOT displayed.")

            # Click on "Cancel"
            cancelBtn = chrome_driver.find_element(By.XPATH, "//button[contains(.,'Cancel')]")
            chrome_driver.execute_script("arguments[0].click();", cancelBtn)

            recordNumber += 1

        except TimeoutException:
            # Check if there is a "Next page" button:
            page_number += 1
            try:
                next_page_button = chrome_driver.find_element(By.XPATH, f"//button[contains(.,'{page_number}')]")
                # Click on the "Next Page" button
                chrome_driver.execute_script("arguments[0].click();", next_page_button)

                print(f"Moving to page {page_number}")
                # Reset the record number:
                recordNumber = 1
            except NoSuchElementException:
                # No more pages, exit the loop
                print("No more pages to process.")
                break

        delay()


def return_to_board_page(chrome_driver):
    try:
        brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
        brand_button.click()
        print("Back to Dashboard.")
        delay()
    except NoSuchElementException as e:
        print(f'Error: {e}')


# ====================================================
def test_verify_edit_icons(chrome_driver, login, roster_element, employees_screen_open):
    entries_per_page_number(chrome_driver)
    all_records_display(chrome_driver)
    return_to_board_page(chrome_driver)
