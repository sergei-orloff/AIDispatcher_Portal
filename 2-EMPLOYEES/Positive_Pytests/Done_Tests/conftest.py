import configparser
import pytest
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Website address:
@pytest.fixture(scope="session")
def website_url():
    return "https://test.aidispatcher.com/authentication"


@pytest.fixture(scope="session")
def chrome_driver(request, website_url):
    chrome_opt = Options()
    chrome_opt.page_load_strategy = 'eager'

    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.WebDriver(service=webdriver_service, options=chrome_opt)

    driver.get(website_url)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def login_credentials():
    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['credentials']['username']
    password = config['credentials']['password']
    return {'username': username, 'password': password}


@pytest.fixture(scope="session")
def login(chrome_driver, login_credentials):
    driver = chrome_driver
    username = login_credentials['username']
    password = login_credentials['password']

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
        print("\nThe 'Board' page is displayed.")
    except TimeoutException:
        print("\nThe 'Board' page is not displayed.")


@pytest.fixture(scope="session")
def roster_element(chrome_driver):
    try:
        element = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))
        chrome_driver.execute_script("arguments[0].click();", element)
        print('\nThe "Roster" element is visible and clickable')
    except TimeoutException:
        print('\nThe "Roster" element is NOT visible or clickable')


@pytest.fixture(scope="session")
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
