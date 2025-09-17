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

    def start_driver(self, start_in_production = None, page_load_strategy='none', loadImage = False, use_undected_chrome_driver = False):
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

        if loadImage is False:
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
            
            Utils.print_with_time(f"Iniciando driver - {session_name} - Produção")
        else:
            if use_undected_chrome_driver:
                self.update_driver(uc.Chrome(options=options))
            else:
                self.update_driver(webdriver.Chrome(options=options))

            Utils.print_with_time(f"Iniciando driver - {session_name} - Local")
        
        return self
    
    def start_thread(self):
        try:
            self.GeneralExecution.start(self.running)
        except Exception as e:
            errorStr = str(e)
            if 'Unable to find session with ID' in errorStr or 'Could not start a new session. Could not start a new session.' in errorStr:
                self.ConsultationExecution.stop()
            else:
                Utils.print_with_time(f"Erro ao executar o loop de execução geral - finalizando\nErro:{e}")
            self.GeneralExecution.stop()
            return
        
        self.quit_driver()
        Utils.print_with_time(f"Finalizando driver - {self.session_name}")
        
    def running(self):
        response = self.execucao_geral()
        if response is not None:
            return response
        
        if self.get_driver() is None:
            Utils.print_with_time("Driver não foi localizado - reiniciando")
            return "CONTINUE"
        try:
            self.ConsultationExecution.start(self.execucao_consulta)
        except Exception as e:
            self.ConsultationExecution.stop()
            Utils.print_with_time(f"Erro ao executar a consulta: {e}") 
    
    @abstractmethod
    def execucao_geral():
        pass

    @abstractmethod
    def execucao_consulta():
        pass

