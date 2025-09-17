from abc import abstractmethod
import time
from selenium import webdriver
from core.Loop import Loop
from core.Utils import Utils
from automation.SeleniumDriver import SeleniumDriver
from integrations.MySqlConnection import MySqlConnection
import undetected_chromedriver as uc

class Selenoid(SeleniumDriver, MySqlConnection):
    ExecucaoGeral = Loop()
    ExecucaoConsulta = Loop()
    
    def __init__(self, options=None):
        super().__init__(options)

    @staticmethod
    def is_driver_valid(driver):
        try:
            return driver is not None and driver.session_id
        except:
            return False

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

        if self.is_driver_valid(driver) == False:
            return
        return self
    
    def start_thread(self):
        Utils.print_with_time(f"bancoDados: {self.bancoDados} - tabela: {self.tabela} - idExecucao: {self.idExecucao} - userId: {self.userId}")
        try:
            self.ExecucaoGeral.start(self.running)
        except Exception as e:
            Utils.print_with_time("Erro ao executar o loop de execução geral - finalizando")
            self.ExecucaoGeral.stop()
        
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
            self.ExecucaoConsulta.start(self.execucao_consulta)
        except Exception as e:
            self.ExecucaoConsulta.stop()
            Utils.print_with_time(f"Erro ao executar a consulta: {e}") 
    
    @abstractmethod
    def execucao_geral():
        pass

    @abstractmethod
    def execucao_consulta():
        pass