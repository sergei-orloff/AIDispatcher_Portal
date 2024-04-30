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
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    except TimeoutException:
        print("The 'Board' page is not displayed.")

    yield driver

    driver.quit()


def test_dispatch_board(chrome_driver):
    pass


def test_freight_load(chrome_driver):
    # Wait until the "Freight" element is visible and clickable
    element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "// span[contains(., 'inventory_2')]")))
    # Click on the element using JavaScript
    chrome_driver.execute_script("arguments[0].click();", element)

    # Verify that the page title is "Loads".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'loads')]")))
        print("The 'Loads' page is displayed.")
    except TimeoutException:
        print("The 'Loads' page is not displayed.")

    # Return to the Board page
    brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
    brand_button.click()
    # Verify that the page title is "Board".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
        print("Back to the 'Board' page.")
    except TimeoutException:
        print("The 'Board' page is not displayed.")
    delay()


def test_connections(chrome_driver):
    # Wait until the "Connections" element is visible and clickable
    element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'hub')]")))
    # Click on the element using JavaScript
    chrome_driver.execute_script("arguments[0].click();", element)

    # Verify that the page title is "Integrations".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'integrations')]")))
        print("The 'Integrations' page is displayed.")
    except TimeoutException:
        print("The 'Integrations' page is not displayed.")

    # Return to the Board page
    brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
    brand_button.click()
    # Verify that the page title is "Board".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
        print("Back to the 'Board' page.")
    except TimeoutException:
        print("The 'Board' page is not displayed.")


def test_roster(chrome_driver):
    # Wait until the "Roster" element is visible and clickable
    element = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))
    # Click on the element using JavaScript
    chrome_driver.execute_script("arguments[0].click();", element)
    print('The "Roster" element is visible and clickable')

    # Return to the Board page
    brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
    brand_button.click()
    # Verify that the page title is "Board".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
        print("Back to the 'Board' page.")
    except TimeoutException:
        print("The 'Board' page is not displayed.")


def test_employees(chrome_driver):
    # Wait until the "Roster" element is visible and clickable
    element = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))

    # Click on the element using JavaScript
    chrome_driver.execute_script("arguments[0].click();", element)

    # Wait until the "Employees" element is clickable and click on it
    element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1nyrutf .MuiTypography-root")))
    element.click()

    chrome_driver.minimize_window()
    chrome_driver.maximize_window()

    # Verify that the page title is "Employees".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'employees')]")))
        print("The 'Employees' page is displayed.")
    except TimeoutException:
        print("The 'Employees' page is not displayed.")

    # Return to the Board page
    brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
    brand_button.click()
    # Verify that the page title is "Board".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
        print("Back to the 'Board' page.")
    except TimeoutException:
        print("The 'Board' page is not displayed.")


def test_assets(chrome_driver):
    # Wait until the "Roster" element is visible and clickable
    element = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))
    # Click on the element using JavaScript
    chrome_driver.execute_script("arguments[0].click();", element)

    # Wait until the "Assets" element is clickable and click on it
    element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Assets')]")))
    element.click()

    chrome_driver.minimize_window()
    chrome_driver.maximize_window()

    # Verify that the page title is "Assets".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'assets')]")))
        print("The 'Assets' page is displayed.")
    except TimeoutException:
        print("The 'Assets' page is not displayed.")

    # Return to the Board page
    brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
    brand_button.click()
    # Verify that the page title is "Board".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
        print("Back to the 'Board' page.")
    except TimeoutException:
        print("The 'Board' page is not displayed.")


def test_groups(chrome_driver):
    # Wait until the "Roster" element is visible and clickable
    element = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))
    # Click on the element using JavaScript
    chrome_driver.execute_script("arguments[0].click();", element)

    # Wait until the "Groups" element is clickable and click on it
    element = WebDriverWait(chrome_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Groups')]")))
    element.click()

    # Verify that the page title is "Groups".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'groups')]")))
        print("The 'Groups' page is displayed.")
    except TimeoutException:
        print("The 'Groups' page is not displayed.")

    # Return to the Board page
    brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
    brand_button.click()
    # Verify that the page title is "Board".
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
        print("Back to the 'Board' page.")
    except TimeoutException:
        print("The 'Board' page is not displayed.")

