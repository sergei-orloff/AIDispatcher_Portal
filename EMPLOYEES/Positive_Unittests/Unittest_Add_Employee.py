"""TestCase class, with separate test methods for logging in and adding an employee. The setUp() method is called
before each test method to set up the test environment, and the tearDown() method is called after each test method to
clean up resources."""
import random
import time
import unittest
from faker import Faker
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


class TestWebAutomation(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()
        chrome_opt = Options()
        Options.age_load_strategy = 'eager'
        # chrome_opt.add_argument("--headless")  # Ensure GUI is off
        # chrome_opt.add_argument("--no-sandbox")
        # chrome_opt.add_argument("--disable-dev-shm-usage")

        webdriver_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.WebDriver(service=webdriver_service, options=chrome_opt)
        self.url = "https://test.aidispatcher.com/authentication"
        self.driver.get(self.url)
        self.driver.maximize_window()

    def test01_login(self):

        # ........ Find the username input field and enter the username
        username_input = self.driver.find_element(By.ID, ":r0:")
        username_input.send_keys("thedogzog@gmail.com")
        # ........ Find the password input field and enter the password
        password_input = self.driver.find_element(By.ID, ":r1:")
        password_input.send_keys("qaz123")
        # ........ Click on the login button
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".MuiButton-root")
        login_button.click()

        # ========================== Verify that the page title is "Board".  =========================
        try:
            # Wait until the element with XPath "//h6[contains(text(),'board')]" is visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'board')]")))
            print("The 'Board' page is displayed.")
        except TimeoutException:
            print("The 'Board' page is not displayed.")

        # ............  Wait until the "Roster" element with class "css-r7rlel" is visible and clickable
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-r7rlel")))

        # Click on the element using JavaScript
        self.driver.execute_script("arguments[0].click();", element)

        # ............  Wait until the "Employees" element with class "css-1nyrutf" is clickable and click on it
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1nyrutf .MuiTypography-root")))
        element.click()

        # ========================== Verify that the page title is "Employees".  =========================
        try:
            # Wait until the page title "Employees" with XPath "//h6[contains(.,'employees')]" is visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h6[contains(.,'employees')]")))
            print("The 'Employees' page is displayed.")
        except TimeoutException:
            print("The 'Employees' page is not displayed.")

        delay()

        # Click on the "Add Employee" button
        add_employee_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".css-cz6ae8 > .MuiButtonBase-root:nth-child(3) > .material-icons-round"))
        )
        add_employee_btn.click()

        # ========================Fill up the form =======================
        delay()

        # .......... First Name..............
        try:
            fName = self.fake.first_name()
            self.driver.find_element(By.XPATH, "//input[@name='firstName']").send_keys(fName)
            print(f"First Name:  {fName}")
        except NoSuchElementException:
            print('No FName field')

        # .......... Last Name...................
        try:
            lName = self.fake.last_name()
            self.driver.find_element(By.XPATH, "//input[@name='lastName']").send_keys(lName)
            print(f"Last Name:  {lName}")
        except NoSuchElementException:
            print('No LName field')

        # .......... Phone number..........
        try:
            phoneNumber = random.randint(2222222222, 9999999999)
            # phoneNumber = fake.basic_phone_number()
            self.driver.find_element(By.XPATH, "//input[@name='contact.phone']").send_keys(str(phoneNumber))
            print(f"Phone Number: {phoneNumber}")
        except NoSuchElementException:
            print('No phoneNumber field')

        # ............... Extension ....................
        try:
            extension = random.randint(1111, 9999)
            self.driver.find_element(By.XPATH, "//input[@name='contact.extension']").send_keys(str(extension))
            print(f"Extension: {extension}")
        except NoSuchElementException:
            print('No extension field')

        # .......... Email..................
        try:
            eMail = self.fake.email()
            self.driver.find_element(By.XPATH, "//input[@name='contact.email']").send_keys(eMail)
            print(f"Email: {eMail}")
        except NoSuchElementException:
            print('No eMail field')

        # ............... Fax ....................
        try:
            fax = random.randint(2222222222, 9999999999)
            # phoneNumber = fake.basic_phone_number()
            self.driver.find_element(By.XPATH, "//input[@name='contact.fax']").send_keys(str(fax))
            print(f"Fax Number: {fax}")
        except NoSuchElementException:
            print('No Fax field')

        # .......... City..............
        try:
            city = self.fake.city()
            self.driver.find_element(By.XPATH, "//input[@name='address.city']").send_keys(city)
            print(f"City: {city}")
        except NoSuchElementException:
            print('No City field')

        # =========== Select a State ========================

        try:
            # ... Click on the dropdown arrow
            find_state = self.driver.find_element(By.XPATH, "// input[ @ name = 'address.state']")
            print("The dropdown arrow found.")
            find_state.click()
            print("The dropdown arrow clicked")
            # Find the desired state option
            find_state = self.driver.find_element(By.XPATH, "// input[ @ name = 'address.state']")
            find_state.clear()
            state = self.fake.state_abbr()
            find_state.send_keys(state)
            # ... Wait for the suggestion to appear using an appropriate wait condition:
            try:
                option_ak = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located(
                        (By.XPATH, "//ul[contains(@class, 'MuiAutocomplete-list')]/li")))
                # Iterate through the autocomplete options and click on the one containing "AK"
                for option in option_ak:
                    if state in option.text:
                        print(f"State: {state}")
                        option.click()
                        break
            except TimeoutException:
                print(f"Element with text {state} not found within the timeout period.")

            find_state.send_keys(Keys.TAB)
        except NoSuchElementException:
            print("Could not locate the dropdown arrow")

        # ========================================================================
        # .......... Zip Code..............
        try:
            zipCode = self.fake.zipcode()
            self.driver.find_element(By.XPATH, "//input[@name='address.zip']").send_keys(zipCode)
            print(f"Zipcode: {zipCode}")
        except NoSuchElementException:
            print('No zipCode field')
        delay()

        # ..........................After filling out the form, Click "Submit" button................
        delay()
        try:
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            print("Submitted")
        except NoSuchElementException:
            print('No submit button found')

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
