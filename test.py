from Resources.SeleniumGrid import SeleniumGrid
from Resources.core.Utils import Utils
from selenium.webdriver.common.by import By

def auto_run(cls):
    instance = cls()  
    instance.start_thread()
    return cls

@auto_run
class test(SeleniumGrid):
    session_name = "test"
    consult_table_name = ""
    result_table_name = ""
    information_to_consult = None

    TARGET_URL = ""
    MAX_COUNT_ERRORS = 4
    ACTUAL_COUNT_ERROR = MAX_COUNT_ERRORS

    def execucao_geral(self):
        Utils.print_with_time(f"Starting General Execution - {self.GeneralExecution.current_position}")
        try:
            if self.GeneralExecution.is_first():
                self.options.add('--remote-debugging-port=9222')
            self.start_driver() 
            if self.execute_login() is False:
                raise Exception("Error in execution of login")
        except Exception as e:
            self.ACTUAL_COUNT_ERROR -= 1
            if self.ACTUAL_COUNT_ERROR > 0:
                Utils.print_with_time(f"Error in starting driver:{e} - Trying againg - {self.ACTUAL_COUNT_ERROR} / {self.MAX_COUNT_ERRORS}")
                return "CONTINUE"
            return "BREAK"

    def execute_login(self, MAX_COUNT_ERRORS = 3):
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
                if MAX_COUNT_ERRORS > 0:
                    Utils.print_with_time("Trying again")
                    return self.execute_login(MAX_COUNT_ERRORS)
                return False

            Utils.print_with_time("User logged in")
            return True
        
        except Exception as e:
            Utils.print_with_time(f"Error in execute login: {e}")
            MAX_COUNT_ERRORS -= 1

            if MAX_COUNT_ERRORS > 0:
                Utils.print_with_time("Trying execute login again")
                return self.execute_login(MAX_COUNT_ERRORS)
            Utils.print_with_time("Fail in execute login, finalizing.")
            return False

    def execucao_consulta(self):
        Utils.print_with_time(f"Starting execution of consult - {self.ConsultationExecution.current_position}")

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
            Utils.print_with_time(f"Error in execution of consults - attempts {max_errors} - {e}")
            if max_errors > 0:
                return self.execute_consult(max_errors=max_errors-1)
            return False