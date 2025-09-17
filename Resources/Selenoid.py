from abc import abstractmethod
import time
from selenium import webdriver
from core.Loop import Loop
from core.Utils import Utils
from automation.SeleniumDriver import SeleniumDriver
from integrations.MySqlConnection import MySqlConnection
import undetected_chromedriver as uc

class Selenoid(SeleniumDriver, MySqlConnection):

    GeneralExecution = Loop()
    ConsultationExecution = Loop()
    
    def __init__(self, options=None):
        super().__init__(options)

    def start_driver(self, start_in_production = None, page_load_strategy='none', loadImage = True, use_undected_chrome_driver = False):
        driver = self.get_driver()
        if driver is not None:
            self.quit_driver()

        if use_undected_chrome_driver:
            options = self.options.undected_chrome_options()
        else:
            options = self.options.chrome_options()
            
        options.page_load_strategy = page_load_strategy

        if loadImage is False:
            options.add_argument("--blink-settings=imagesEnabled=false")
        
        session_name = self.session_name + "_" + str(int(time.time()))
        # options.set_capability('browserVersion', '128.0')
        options.set_capability('selenoid:options', {
            'enableVNC': True, 'enableVideo': False, 'name': session_name})
        
        start_in_production = self.start_in_production if start_in_production is None else start_in_production
        if start_in_production:
            if use_undected_chrome_driver:
                capabilities = options.to_capabilities()
                self.update_driver(webdriver.Remote(command_executor=Utils.get_env('SELENOID_URL'), capabilities=capabilities)) 
            else:
                self.update_driver(webdriver.Remote(command_executor=Utils.get_env('SELENOID_URL'), options=options)) 
        else:
            if use_undected_chrome_driver:
                self.update_driver(uc.Chrome(options=options))
            else:
                self.update_driver(webdriver.Chrome(options=options))

        return self
    
    def start_thread(self):
        try:
            self.GeneralExecution.start(self.running)
        except Exception as e:
            Utils.print_with_time("Error executing the general execution loop - finishing")
            self.GeneralExecution.stop()
        
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