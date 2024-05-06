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

        # ............Read the names from the JSON file  .............
        print("The list of names loaded.")

        # Extract the first name from the JSON data
        self.name_to_delete = load_name["names"][0]
        print(f"Name '{self.name_to_delete}' extracted.")

    def find_the_employee_to_delete(self):

        # Search the employee to delete:
        search_box = self.chrome_driver.find_element(By.XPATH, "//input[contains(@name,'search')]")
        search_box.send_keys(self.name_to_delete)
        print(f"Name to delete: {self.name_to_delete}")

        delay()

        # Verify the name by First Name and Last Name:
        name_displayed = self.chrome_driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]").text
        print(f"Name displayed: {name_displayed}")

        delay()
        try:
            assert name_displayed == self.name_to_delete
            print("Correct name to delete")
        except AssertionError:
            print("Wrong name!")

    def update_names_list(self):
        # --------- Update the list of names: --------------
        names_list_file = "names_list.json"
        # Remove the desired name
        name_to_remove = self.name_to_delete
        if name_to_remove in self.load_name['names']:
            self.load_name['names'].remove(name_to_remove)
            print(f"Value '{name_to_remove}' removed successfully.")

            # Write the modified data back to the JSON file
            with open(names_list_file, 'w') as json_file:
                json.dump(self.load_name, json_file, indent=2)
                print("Names updated and written to JSON file.")
        else:
            print(f"Value '{name_to_remove}' not found.")


def ready_to_delete_employee(chrome_driver):
    # Locate the Delete icon:
    try:
        delete_icon = chrome_driver.find_element(By.XPATH, "//span[contains(.,'delete')]")
        delete_icon.click()
        delay()
        print("Delete icon found!")
        # print(f"The employee '{self.name_to_delete}' is deleted.")
    except NoSuchElementException:
        print("No delete icon found!")
    # ------ Verify the Pop-up message:
    try:
        pop_up = WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "// p[contains(., 'Do you want to delete the employee?')]")))
        print(f"The '{pop_up.text} displayed.'")
    except NoSuchElementException:
        print(f"No pop-up message displayed!")

#
# # ------ Options: To Cancel or to Delete: ---------------
# def cancel_delete_button(chrome_driver):
#     # -------- Pop-up screen ==> Click "Cancel" button:
#     cancel_button = chrome_driver.find_element(By.XPATH, "//button[contains(.,'Cancel')]")
#     cancel_button.click()
#     print("Delete canceled.")
#     delay()
#     # return True


def delete_confirm(chrome_driver):
    # -------- Pop-up screen ==> Click "Delete" button:
    delete_button = chrome_driver.find_element(By.XPATH, "//button[contains(.,'Delete')]")
    delete_button.click()
    print("The 'Delete' button clicked.")
    delay()


# --------- Back to the Dashboard: ------------------------
def return_to_board_page(chrome_driver):
    try:
        brand_button = chrome_driver.find_element(By.XPATH, "//img[contains(@alt,'Brand')]")
        brand_button.click()
        print("Back to Dashboard.")
    except NoSuchElementException as e:
        print(f'Error: {e}')


# =====================================================================
def test_delete_employee(chrome_driver, login, roster_element, employees_screen_open):
    locate_search_box(chrome_driver)
    clear_search_field(chrome_driver)
    # -------------------------------------------
    with open("names_list.json", "r") as json_file:
        load_name = json.load(json_file)
    actions = EmployeeActions(chrome_driver, load_name)
    actions.find_the_employee_to_delete()
    ready_to_delete_employee(chrome_driver)

    # ------ Options: To Cancel or to Delete: ---------------
    delete_confirm(chrome_driver)

    # ------- Update the list of names: ----------
    actions.update_names_list()

    # --------- Back to the Dashboard: ---------------------------------
    return_to_board_page(chrome_driver)
