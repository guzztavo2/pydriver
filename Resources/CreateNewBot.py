import os
import sys
import time
from core.Utils import Utils

def selections(message:str, selections:list = None):
    actual_selection = 0
    selections_ = [0] * len(selections)
    while True:
        print("\n" + message)
        for key,val in enumerate(selections):
            if key == actual_selection:
                print(f"> {key} - {val}")
            else:
                print(f"  {key} - {val}")
            selections_[key] = key

        selection = get_value("\nSelection: ", selections_, False, True)
        os.system('cls') if os.name == 'nt' else os.system('clear')
        if actual_selection == selection:
            return selection
        actual_selection = selection
        
def get_value(message, expected_results = None, onlyLetters = None, onlyNumbers = None):
    result = None
    while result is None or (expected_results is not None and result not in expected_results):
        result = Utils.get_input(message, onlyLetters, onlyNumbers)
        if expected_results is not None:
            if result not in expected_results:
                print("Value not selected successfully, trying again")
                simulate_loading()
                continue
        if onlyLetters is not None or onlyNumbers is not None:
            if len(str(result)) <= 0:
                continue
        break
    return result

def simulate_loading():
    for i in range(50):
        print('.', end='', flush=True)
        time.sleep(0.01)
    print("\n")

def select_directories(actual_path = '../'):
    actual_path = os.path.abspath(actual_path)
    list_dirs = ["... (back directory)", f"{actual_path[actual_path.rfind('/') + 1:]} (actual directory)"]
    list_dirs += [dir.name for dir in list(os.scandir(actual_path)) if dir.is_dir()]
    
    selected_dir = selections("\nSelected de folder you need:",list_dirs)

    if selected_dir == 0:
        return select_directories(actual_path[:actual_path.rfind('/')])
    elif selected_dir == 1:
        Utils.print_with_time(f"Path chosen: {actual_path}")
        return actual_path
    else:
        return select_directories(actual_path + f'/{list_dirs[selected_dir]}')

def create_env_file(dir_path):
    create_env = get_value("It was not possible to locate the env, would you like to create a structure?\n\t0 - Yes\t1 - Nop\nSelection:", expected_results=[0,1], onlyNumbers=True)
    if create_env == 0:
        try:
            Utils.print_with_time(f"Creating {dir_path}")
            dataToEnv = """
                    START_IN_PRODUCTION=False
                    #False executes in a local environment and True executes in a production environment using the SELENIUMGRID_URL or SELENOID_URL of the application.
                    API_URL=
                    SELENIUMGRID_URL=
                    SELENOID_URL=
                    MYSQL_IN_PRODUCTION=False
                    #False executes in a local environment and True executes in a production environment.

                    MYSQL_HOST_TEST=*********
                    MYSQL_USER_TEST=*********
                    MYSQL_PASSWORD_TEST=*********
                    MYSQL_DATABASE_TEST=*********

                    MYSQL_HOST_PRODUCTION=*********
                    MYSQL_USER_PRODUCTION=*********
                    MYSQL_PASSWORD_PRODUCTION=*********
                    MYSQL_DATABASE_PRODUCTION=*********

                    CHROME_BINARY_LOCATION=/usr/bin/chromium
                    HOUR_FORMAT=%d/%m/%Y %H:%M:%S
                    """
            Utils.create_file_insert_data(f"{dir_path}", dataToEnv)
            Utils.print_with_time(f"Created successfully: {dir_path}")
        except Exception as e:
            Utils.print_with_time(f"Error creating: {dir_path}: {e}")

Utils.print_with_time("Trying to locate the environment variables (.env)")
simulate_loading()
DIR_ENV = os.path.abspath("./Resources/.env")
if os.path.exists(DIR_ENV) is False:
   create_env_file(DIR_ENV)
else:
    Utils.print_with_time(f"Successfully located Env {DIR_ENV}")

simulate_loading()

folder_path = select_directories()

selenium_type = selections("\nSelected de folder you need:",['Selenoid', 'Selenium Grid'])
simulate_loading()
botName = get_value("Enter your bot's name:", onlyLetters=True)
TARGET_URL = get_value("Bot's Target url: ")
simulate_loading()
selenium_type = "SeleniumGrid" if selenium_type == 1 else "Selenoid"
botStr = botName
script = f"""
from Resources.{selenium_type} import {selenium_type}
from Resources.core.Utils import Utils
from selenium.webdriver.common.by import By

def auto_run(cls):
    instance = cls()  
    instance.start_thread()
    return cls

@auto_run
class {botName}({selenium_type}):
    session_name = "{botStr}"
    
    consult_table_name = ""
    result_table_name = ""
    information_to_consult = None

    TARGET_URL = "{TARGET_URL}"
    MAX_COUNT_ERRORS = 4
    ACTUAL_COUNT_ERROR = MAX_COUNT_ERRORS
    
    def before_start_loop(self):
        self.start_proxies()

    def start_proxies():
        proxyIpList = ["ip1", "ip2"]
        proxyPortList = ["port1", "port2"]
        proxyUsernameList = ["user1", "user2"]
        proxyPasswordList = ["pass1", "pass2"]
        ProxyOption.array_to_proxies(proxyIpList, proxyPortList, proxyUsernameList, proxyPasswordList)

    def general_execution(self):
        Utils.print_with_time(f"Starting General Execution - {{self.GeneralExecution.current_position}}")
        try:
            # if self.GeneralExecution.is_first():
                # self.options.add('--remote-debugging-port=9222')
                # self.start_proxies()
            self.start_driver(page_load_strategy='none', load_images = False, use_undected_chrome_driver = False) 
            if self.execute_login() is False:
                raise Exception("Error in execution of login")
        except Exception as e:
            self.ACTUAL_COUNT_ERROR -= 1
            if self.ACTUAL_COUNT_ERROR > 0:
                Utils.print_with_time(f"Error in starting driver:{{e}} - Trying againg - {{self.ACTUAL_COUNT_ERROR}} / {{self.MAX_COUNT_ERRORS}}")
                return "CONTINUE"
            return "BREAK"

    def execute_login(self, max_login_errors = 3):
        try:
            driver = self.get_driver()
            if self.TARGET_URL not in driver.current_url:
                if self.navigate_to_url(self.TARGET_URL) is False:
                    raise Exception("Not possible access page of login.")

            self.send_keys_into_element("user_element", self.user.get_username())
            self.send_keys_into_element("password_element", self.user.get_password())
            self.click_element("submit_login", By.XPATH)
            self.wait_page_loading()

            if "url of the result login" not in driver.current_url:
                Utils.print_with_time("Not possible access login...")
                if max_login_errors > 0:
                    Utils.print_with_time("Trying again")
                    return self.execute_login(max_login_errors)
                return False

            Utils.print_with_time("User logged in")
            return True
        
        except Exception as e:
            Utils.print_with_time(f"Error in execute login: {{e}}")
            max_login_errors -= 1

            if max_login_errors > 0:
                Utils.print_with_time("Trying execute login again")
                return self.execute_login(max_login_errors)
            Utils.print_with_time("Fail in execute login, finalizing.")
            return False

    def consult_execution(self):
        Utils.print_with_time(f"Starting execution of consult - {{self.ConsultationExecution.current_position}}")

        if self.information_to_consult is None:
            self.information_to_consult = self.fetch_data()
            if self.information_to_consult is False:
                self.information_to_consult = None
                return "CONTINUE"
        
        responseOfConsultation = self.execute_consult()

        if responseOfConsultation is False:
            Utils.print_with_time("Fail in execution of consult")
            if self.ACTUAL_COUNT_ERROR <= 0:
                Utils.print_with_time("Restart driver")
                return "BREAK"

            self.ACTUAL_COUNT_ERROR -= 1
            Utils.print_with_time("Trying again!")
            return "CONTINUE"
        elif responseOfConsultation == "FAIL":
            return "BREAK"
        
        return "CONTINUE"

    def execute_consult(self, max_errors = 3):
        try:
            pass
        except Exception as e:
            Utils.print_with_time(f"Error in execution of consult - attempts {{max_errors}} - {{e}}")
            if max_errors > 0:
                return self.execute_consult(max_errors=max_errors-1)
            return False
"""

try:
    Utils.create_file_insert_data(os.path.abspath(folder_path + f"/{botName}.py"), script)
    Utils.print_with_time(f"Archive created with successful: " + os.path.abspath(folder_path + f"/{botName}.py"))
except Exception as e:
    Utils.print_with_time(f"Error creating file: {e}")
finally:
    simulate_loading()
    Utils.print_with_time("Finalizing application.")
    sys.exit(0)
