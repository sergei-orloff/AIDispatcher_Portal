import random
import time
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome import ChromeDriverManager, webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


def delay():
    time.sleep(random.randint(1, 3))  # Delay all actions from 1 to 3 sec


@pytest.fixture(scope="session")
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
        # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    except TimeoutException:
        print("The 'Board' page is not displayed.")

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def roster_element(chrome_driver):
    try:
        element = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))
        chrome_driver.execute_script("arguments[0].click();", element)
        print('The "Roster" element is visible and clickable')
    except TimeoutException:
        print('The "Roster" element is NOT visible or clickable')


def navigate_to_section(chrome_driver, section_text):
    try:
        element = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(.,'{section_text}')]")))
        # Click on the element using JavaScript
        chrome_driver.execute_script("arguments[0].click();", element)
    except TimeoutException as e:
        print(f'Error: {e}')


def max_min_window(chrome_driver):
    chrome_driver.minimize_window()
    chrome_driver.maximize_window()


def verify_page_title(chrome_driver, expected_title):
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//h6[contains(.,'{expected_title.lower()}')]")))
        print(f"The '{expected_title.capitalize()}' page is displayed.")
    except TimeoutException:
        print(f"The '{expected_title.capitalize()}' page is not displayed.")


def return_to_board_page(chrome_driver):
    try:
        brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
        brand_button.click()
    except NoSuchElementException as e:
        print(f'Error: {e}')


@pytest.mark.parametrize("section_text, expected_title", [
                                                            ("Freight", "loads"),
                                                            ("Connections", "integrations"),
                                                            ("Employees", "Employees"),
                                                            ("Assets", "Assets"),
                                                            ("Groups", "Groups")
                                                         ])
def test_all_screens_navigation(chrome_driver, roster_element, section_text, expected_title):
    navigate_to_section(chrome_driver, section_text)
    max_min_window(chrome_driver)
    verify_page_title(chrome_driver, expected_title)
    delay()
    return_to_board_page(chrome_driver)

