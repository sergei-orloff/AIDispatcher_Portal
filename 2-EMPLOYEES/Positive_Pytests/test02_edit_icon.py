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
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def chrome_driver():
    faker = Faker()
    chrome_opt = Options()
    Options.age_load_strategy = 'eager'
    # chrome_opt.add_argument("--headless")  # Ensure GUI is off
    # chrome_opt.add_argument("--no-sandbox")
    # chrome_opt.add_argument("--disable-dev-shm-usage")

    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.WebDriver(service=webdriver_service, options=chrome_opt)
    url = "https://test.aidispatcher.com/authentication"
    driver.get(url)
    driver.maximize_window()

    # LogIn Credentials
    username = "thedogzog@gmail.com"
    password = "qaz123"

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

    # Wait until the "Roster" element is visible and clickable
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))

    # Click on the element using JavaScript
    driver.execute_script("arguments[0].click();", element)

    # Wait until the "Employees" element is clickable and click on it
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1nyrutf .MuiTypography-root")))
    element.click()

    # Verify that the page title is "Employees".
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'employees')]")))
        print("The 'Employees' page is displayed.")
    except TimeoutException:
        print("The 'Employees' page is not displayed.")

    yield driver

    driver.quit()


def delay():
    time.sleep(random.randint(1, 3))  # Delay all actions from 1 to 3 sec


def test_edit_icon(chrome_driver):
    # Optional: Find the number of Entries per page
    setEntriesNumber = chrome_driver.find_element(By.ID, ":re:")

    # Read the number of entries per page in the combobox:
    entriesPerPage = setEntriesNumber.get_attribute("value")

    print("The number of entries per page is up to:", entriesPerPage)
    # Loop through the pages:
    page_number = 1
    recordNumber = 1
    while True:
        record_xpath = f"(//span[contains(., 'edit')])[{recordNumber}]"

        # Process all records on the page:
        try:
            # Wait for the "Edit" icon to be present:
            edit_icon = WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.XPATH, record_xpath)))
            # Click on the "Edit" icon:
            chrome_driver.execute_script("arguments[0].click();", edit_icon)

            delay()
            # Verify the form title == "Employee Info"
            try:
                title = chrome_driver.find_element(By.XPATH, "//h3[contains(.,'Employee Info')]")

                fNameBox = chrome_driver.find_element(By.XPATH, "//input[@name='firstName']")
                # Read the First name
                firstName = fNameBox.get_attribute("value")

                lNameBox = chrome_driver.find_element(By.XPATH, "//input[@name='lastName']")
                # Read the Last name
                lastName = lNameBox.get_attribute("value")

                print(f"'{title.text}':  {firstName} {lastName}")
            except NoSuchElementException:
                print(f"The form 'Employee Info' is NOT displayed.")
            # Click on "Cancel"
            cancelBtn = chrome_driver.find_element(By.XPATH, "//button[contains(.,'Cancel')]")
            cancelBtn.click()

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
