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

# Website address:
url = "https://test.aidispatcher.com/authentication"
# LogIn Credentials
username = "thedogzog@gmail.com"
password = "qaz123"


@pytest.fixture(scope="session")
def chrome_driver(request):
    chrome_opt = Options()
    Options.age_load_strategy = 'eager'

    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.WebDriver(service=webdriver_service, options=chrome_opt)

    driver.get(url)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def login(chrome_driver):
    driver = chrome_driver

    # Find the username input field and enter the username
    username_input = driver.find_element(By.ID, ":r0:")
    username_input.send_keys(username)
    # Find the password input field and enter the password
    password_input = driver.find_element(By.ID, ":r1:")
    password_input.send_keys(password)
    # Click on the login button
    login_button = driver.find_element(By.CSS_SELECTOR, ".MuiButton-root")
    login_button.click()

    # Verify that the page title is "Board".
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
        print("The 'Board' page is displayed.")
    except TimeoutException:
        print("The 'Board' page is not displayed.")


def delay():
    time.sleep(random.randint(1, 2))  # Delay all actions from 1 to 2 sec


def roster_element(chrome_driver):
    try:
        element = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))
        chrome_driver.execute_script("arguments[0].click();", element)
        print('The "Roster" element is visible and clickable')
    except TimeoutException:
        print('The "Roster" element is NOT visible or clickable')


def employees_screen_open(chrome_driver):
    # Wait until the "Employees" element is clickable and click on it
    element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1nyrutf .MuiTypography-root")))
    element.click()

    # Verify that the page title is "Employees".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'employees')]")))
        print("The 'Employees' page is displayed.")
    except TimeoutException:
        print("The 'Employees' page is not displayed.")


# Optional:
def entries_per_page_number(chrome_driver):
    # Optional: Find the number of Entries per page
    try:
        setEntriesNumber = WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, ":re:")))
        # Read the number of entries per page in the combobox:
        entriesPerPage = setEntriesNumber.get_attribute("value")
        print("The number of entries per page is up to:", entriesPerPage)
    except TimeoutException:
        print("Entries number is not visible.")


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

                print(f"'{title.text}':  {firstName} {lastName}")
            except NoSuchElementException:
                print(f"The form 'Employee Info' is NOT displayed.")

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


def test_verify_edit_icons(chrome_driver, login):
    roster_element(chrome_driver)
    employees_screen_open(chrome_driver)
    all_records_display(chrome_driver)
    return_to_board_page(chrome_driver)
