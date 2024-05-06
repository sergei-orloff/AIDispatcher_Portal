import json
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
from selenium.webdriver import Keys


def delay():
    time.sleep(random.randint(1, 2))  # Delay all actions from 1 to 2 sec


def locate_search_box(chrome_driver):
    # Locate the Search box:
    try:
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@name,'search')]")))
        print("The Search box is displayed.")
    except TimeoutException:
        print("The Search box is NOT displayed.")


def clear_search_field(chrome_driver):
    # Clear the Search field
    search_box = chrome_driver.find_element(By.XPATH, "//input[contains(@name,'search')]")
    search_box.clear()

    delay()


class EmployeeActions:
    def __init__(self, chrome_driver, load_name):  # Add load_name parameter to the constructor
        self.chrome_driver = chrome_driver
        self.load_name = load_name  # Store load_name as an instance variable
        self.fake = Faker()
        self.new_name = None  # Define new_name attribute
        # ............Read the names from the JSON file  .............
        print("\nThe list of names loaded.")

    def add_employee(self):  # ===== TC: Verify the "Add Employee" icon and form functionality.

        # Click on the "Add Employee" button
        add_employee_btn = WebDriverWait(self.chrome_driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".css-cz6ae8 > .MuiButtonBase-root:nth-child(3) > .material-icons-round"))
        )
        add_employee_btn.click()

        # ========================Fill up the form =======================
        delay()

        # .......... First Name..............
        try:
            fName = self.fake.first_name()
            self.chrome_driver.find_element(By.XPATH, "//input[@name='firstName']").send_keys(fName)
            print(f"First Name:  {fName}")
        except NoSuchElementException:
            print('No FName field')

        # .......... Last Name...................
        try:
            lName = self.fake.last_name()
            self.chrome_driver.find_element(By.XPATH, "//input[@name='lastName']").send_keys(lName)
            print(f"Last Name:  {lName}")
        except NoSuchElementException:
            print('No LName field')

        # .......... Phone number..........
        try:
            phoneNumber = random.randint(2222222222, 9999999999)
            # phoneNumber = fake.basic_phone_number()
            self.chrome_driver.find_element(By.XPATH, "//input[@name='contact.phone']").send_keys(str(phoneNumber))
            print(f"Phone Number: {phoneNumber}")
        except NoSuchElementException:
            print('No phoneNumber field')

        # ............... Extension ....................
        try:
            extension = random.randint(1111, 9999)
            self.chrome_driver.find_element(By.XPATH, "//input[@name='contact.extension']").send_keys(str(extension))
            print(f"Extension: {extension}")
        except NoSuchElementException:
            print('No extension field')

        # .......... Email..................
        try:
            eMail = self.fake.email()
            self.chrome_driver.find_element(By.XPATH, "//input[@name='contact.email']").send_keys(eMail)
            print(f"Email: {eMail}")
        except NoSuchElementException:
            print('No eMail field')

        # ............... Fax ....................
        try:
            fax = random.randint(2222222222, 9999999999)
            # phoneNumber = fake.basic_phone_number()
            self.chrome_driver.find_element(By.XPATH, "//input[@name='contact.fax']").send_keys(str(fax))
            print(f"Fax Number: {fax}")
        except NoSuchElementException:
            print('No Fax field')

        # .......... City..............
        try:
            city = self.fake.city()
            self.chrome_driver.find_element(By.XPATH, "//input[@name='address.city']").send_keys(city)
            print(f"City: {city}")
        except NoSuchElementException:
            print('No City field')

        # =========== Select a State ========================

        try:
            # ... Click on the dropdown arrow
            find_state = self.chrome_driver.find_element(By.XPATH, "// input[ @ name = 'address.state']")
            print("The dropdown arrow found.")
            find_state.click()
            print("The dropdown arrow clicked")
            # Find the desired state option
            find_state = self.chrome_driver.find_element(By.XPATH, "// input[ @ name = 'address.state']")
            find_state.clear()
            state = self.fake.state_abbr()
            find_state.send_keys(state)
            # ... Wait for the suggestion to appear using an appropriate wait condition:
            try:
                option_ak = WebDriverWait(self.chrome_driver, 10).until(
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
            self.chrome_driver.find_element(By.XPATH, "//input[@name='address.zip']").send_keys(zipCode)
            print(f"Zipcode: {zipCode}")
        except NoSuchElementException:
            print('No zipCode field')
        delay()

        # ..........................After filling out the form, Click "Submit" button................
        delay()
        try:
            self.chrome_driver.find_element(By.XPATH, "//button[@type='submit']").click()
            print("Submitted")
            self.new_name = f"{fName} {lName}"
        except NoSuchElementException:
            print('No submit button found')

        # ---------- Verify the new name is added to the records: ------------

        search_box = self.chrome_driver.find_element(By.XPATH, "//input[contains(@name,'search')]")
        # Clear the Search field
        search_box.clear()
        delay()
        # ----------- Enter the new name: ----------------------------
        search_box.send_keys(self.new_name)
        print(f"The new record: {self.new_name}, has been entered in 'Search'.")

        delay()

        # Verify the name by First Name and Last Name:
        name_displayed = self.chrome_driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]").text
        print(f"Name displayed: {name_displayed}")

        delay()
        try:
            assert name_displayed == self.new_name
            print("Correct name displayed")
        except AssertionError:
            print(f"Wrong name - {name_displayed} - displayed!")
        # ============================================================================================

    def new_employee_entry(self):
        # --------- Update the list of names: --------------
        names_list_file = "names_list.json"
        # --------- Add the new name: -------
        name_to_add = self.new_name

        if name_to_add not in self.load_name['names']:
            self.load_name['names'].append(name_to_add)
            print(f"Employee '{name_to_add}' added to the list successfully.")

            # Write the modified data back to the JSON file
            with open(names_list_file, 'w') as json_file:
                json.dump(self.load_name, json_file, indent=2)
                print("Names updated and written to JSON file.")
        else:
            print(f"The employee '{name_to_add}' record confirmed.")


# --------- Back to the Dashboard: ------------------------
def return_to_board_page(chrome_driver):
    try:
        brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
        brand_button.click()
        print("Back to Dashboard.")
    except NoSuchElementException as e:
        print(f'Error: {e}')


# =====================================================================
def test_add_Employee(chrome_driver, login, roster_element, employees_screen_open):

    with open("names_list.json", "r") as json_file:
        load_name = json.load(json_file)
    actions = EmployeeActions(chrome_driver, load_name)

    # --------Add a new employee: -----------------
    actions.add_employee()
    actions.new_employee_entry()

    # --------- Back to the Dashboard: ---------------------------------
    return_to_board_page(chrome_driver)
