from abc import abstractmethod
import time
from selenium import webdriver
from Resources.automation.SeleniumDriver import SeleniumDriver
from Resources.integrations.MySqlConnection import MySqlConnection
from Resources.integrations.Api import Api
from Resources.core.Utils import Utils
from Resources.core.Loop import Loop
import undetected_chromedriver as uc

class SeleniumGrid(SeleniumDriver, MySqlConnection, Api):
    GeneralExecution = Loop()
    ConsultationExecution = Loop()
    
    def __init__(self, options=None):
        super().__init__(options)

    def start_driver(self, start_in_production = None, page_load_strategy='none', load_images = False, use_undected_chrome_driver = False):
        driver = self.get_driver()
        if driver is not None:
            self.quit_driver()

        capabilities = None
        if use_undected_chrome_driver:
            options = self.options.undected_chrome_options()
        else:
            options = self.options.chrome_options()

        if page_load_strategy is not None:
            options.page_load_strategy = page_load_strategy

        if load_images is False:
            options.add_argument("--blink-settings=imagesEnabled=false")
        session_name = self.session_name + "_" + str(int(time.time()))
        options.set_capability("se:name", session_name)
        start_in_production = self.start_in_production if start_in_production is None else start_in_production

        if start_in_production:
            if use_undected_chrome_driver:
                capabilities = options.to_capabilities()
                self.update_driver(webdriver.Remote(command_executor=Utils.get_env('SELENIUMGRID_URL'), capabilities=capabilities)) 
            else:
                self.update_driver(webdriver.Remote(command_executor=Utils.get_env('SELENIUMGRID_URL'), options=options)) 
            
            Utils.print_with_time(f"Starting driver - {session_name} - Production")
        else:
            if use_undected_chrome_driver:
                self.update_driver(uc.Chrome(options=options))
            else:
                self.update_driver(webdriver.Chrome(options=options))

            Utils.print_with_time(f"Starting driver - {session_name} - Local")
        
        return self
    
    def start_thread(self):
        try:
            self.GeneralExecution.start(self.running)
        except Exception as e:
            errorStr = str(e)
            if 'Unable to find session with ID' in errorStr or 'Could not start a new session. Could not start a new session.' in errorStr:
                self.ConsultationExecution.stop()
            else:
                Utils.print_with_time(f"Error executing the general execution loop - finishing\nError:{e}")
            self.GeneralExecution.stop()
            return
        
        self.quit_driver()
        Utils.print_with_time(f"finishing driver - {self.session_name}")
        
    def running(self):
        response = self.general_execution()
        if response is not None:
            return response
        
        if self.get_driver() is None:
            Utils.print_with_time("Driver not found - restarting")
            return "CONTINUE"
        try:
            self.ConsultationExecution.start(self.consult_execution)
        except Exception as e:
            self.ConsultationExecution.stop()
            Utils.print_with_time(f"Error executing the consultation: {e}") 
    
    @abstractmethod
    def general_execution():
        pass

    @abstractmethod
    def consult_execution():
        pass