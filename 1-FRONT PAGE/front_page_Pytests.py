import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    url = "https://test.aidispatcher.com/authentication"
    driver.get(url)
    driver.maximize_window()
    sleep(3)
    yield driver  # Yield the driver instance, so it can be used by the tests
    driver.quit()  # Quit the driver after the test is done


def test_license_link(chrome_driver):
    # .......... License link .........................
    license_link = chrome_driver.find_element(By.XPATH, "//span[contains(.,'License')]")
    license_link.click()

    # ........... Blog Link .............................


def test_blog_link(chrome_driver):
    blog_link = chrome_driver.find_element(By.XPATH, "//span[contains(.,'Blog')]")
    blog_link.click()


def test_about_link(chrome_driver):
    # ........... About Us Link .............................
    about_link = chrome_driver.find_element(By.XPATH, "//span[contains(.,'About Us')]")
    about_link.click()


def test_west_llc_link(chrome_driver):
    # .......... Westbridge LLC link .........................
    westbridge_link = chrome_driver.find_element(By.XPATH, "//span[contains(.,'Westbridge LLC')]")
    westbridge_link.click()


def test_westbridge_site_link(chrome_driver):
    # .......... Westbridge Website link .........................
    site_link = chrome_driver.find_element(By.XPATH,
                                           "//span[@class='MuiTypography-root MuiTypography-button css-muyete']")
    site_link.click()


sleep(3)
