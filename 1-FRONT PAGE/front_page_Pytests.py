import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep


@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    # Set implicit wait time
    driver.implicitly_wait(3)  # 3 seconds
    url = "https://test.aidispatcher.com/authentication"
    driver.get(url)
    driver.maximize_window()
    sleep(3)
    yield driver  # Yield the driver instance, so it can be used by the tests
    driver.quit()  # Quit the driver after the test is done


def test_front_page_links(chrome_driver):
    link_paths = [
        "//span[contains(.,'Back to AIDispatcher.com')]",
        "//span[contains(.,'License')]",
        "//span[contains(.,'Blog')]",
        "//span[contains(.,'About Us')]",
        "//span[contains(.,'Westbridge LLC')]",
        "//span[@class='MuiTypography-root MuiTypography-button css-muyete']",
        "//a[contains(.,'Sign up')]",
        "//a[contains(.,'Reset Password')]"
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
        "//span[contains(text(), 'have an account?')]"  # (7) 'Don't have an account?'label
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


sleep(3)
