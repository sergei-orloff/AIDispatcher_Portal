"""
Run from the current directory:

         pytest -s
It will display all printouts.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import requests

url = "https://test.aidispatcher.com/authentication"


@pytest.fixture
def chrome_driver():
    global url
    driver = webdriver.Chrome()
    # Set implicit wait time
    driver.implicitly_wait(3)  # 3 seconds
    driver.get(url)
    driver.maximize_window()
    sleep(3)
    yield driver  # Yield the driver instance, so it can be used by the tests
    driver.quit()  # Quit the driver after the test is done


# ......TC-0: Verify the webpage is accessible.........................
def test00_webpage_access(chrome_driver):
    # .........Check that an element is present on the DOM of a page and visible.

    chrome_driver.minimize_window()
    chrome_driver.maximize_window()

    # ................API testing from Selenium....................
    global url
    print("Webpage Url has", requests.get(url).status_code, "as status Code")
    code = requests.get(url).status_code
    if code == 200:
        print("API response code is OK")
    else:
        print("API response code is not 200", "Current code is:", code)

    # .................Check current webpage Title with Exception functionality
    try:
        assert "AIDispatcher" in chrome_driver.title
        print("Webpage is CORRECT. Current Title is: ", chrome_driver.title)
    except AssertionError:
        print("Webpage is different, current Title is: ", chrome_driver.title)


def test_front_page_links(chrome_driver):
    link_paths = [
        "//span[contains(.,'Back to AIDispatcher.com')]",
        "//span[contains(.,'License')]",
        "//span[contains(.,'Blog')]",
        "//span[contains(.,'About Us')]",
        "//span[contains(.,'Westbridge LLC')]",
        "//span[@class='MuiTypography-root MuiTypography-button css-muyete']"
    ]

    for my_link_xpath in link_paths:
        try:
            link = chrome_driver.find_element(By.XPATH, my_link_xpath)
            link_name = link.text
            if link.is_enabled() and link.is_displayed():
                # If an element is clickable, perform actions on it
                print(f"{link_name} is clickable.")
            else:
                print(f"The link {link_name} is NOT clickable.")
        except NoSuchElementException:
            print(f"{link_name} not found within the implicit wait time")


def test_sign_in_form_elements(chrome_driver):
    count = 1
    form_elements = [
        "//h3[contains(.,'Sign In')]",  # (1) the form title
        "//label[contains(text(),'Email')]",  # (2) the email field
        "//label[contains(text(), 'Password')]",  # (3)
        "//span[contains(.,'Remember me')]",  # (4) 'Remember me' label
        "//input[contains(@type,'checkbox')]",  # (5) 'Remember me' checkbox
        "//button[contains(.,'sign in')]",  # (6) 'Sign In' button
        "//a[contains(.,'Sign up')]",  # (7) 'Sign Up' link.
        "//a[contains(.,'Reset Password')]"  # (8) 'Reset Password' link
    ]

    for an_element in form_elements:
        try:
            element = chrome_driver.find_element(By.XPATH, an_element)
            element_name = element.text
            element_type = element.get_attribute('type')
            print(f"No.{count}. {element_type} - '{element_name}' is present.")
        except NoSuchElementException:
            print(f"No.{count}. {element_type} - '{element_name}' NOT visible.")

        count += 1

    # 'Don't have an account?'label
    try:
        label = "Don't have an account?"
        assert label in chrome_driver.page_source
        print(f'The text "{label}" is visible.')
    except AssertionError:
        print(f"{label} is not visible.")


def test_footnote(chrome_driver):
    try:
        footnote = chrome_driver.find_element(By.CLASS_NAME, "css-8ulqt3").text
        # Expected text content with preserved format
        expected_text_content = "© 2024, made with\nfavorite\nby\n Westbridge \nfor a better logistics."

        # Assertion statement to compare the actual text content with the expected text content
        assert footnote == expected_text_content, "Text content does not match the expected content"
        print(f'The content of the footnote -  "{footnote}" - is correct.')
    except Exception as e:
        print(f"An error occurred: {e}")


sleep(3)

"""
Run from the current directory:

         pytest -s
         
It will display all printouts.
"""
