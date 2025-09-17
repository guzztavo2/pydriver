import os
import re
import sys
import platform
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

def select_directories(actual_path = './'):
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

Utils.print_with_time("Trying to locate the environment variables (.env)")
simulate_loading()
DIR_ENV = os.path.abspath("./Resources/.env")
if os.path.exists(DIR_ENV) is False:
    create_env = get_value("It was not possible to locate the env, would you like to create a structure?\n\t0 - Yes\t1 - Nop\nSelection:", expected_results=[0,1], onlyNumbers=True)
    if create_env == 0:
        try:
            Utils.print_with_time(f"Creating {DIR_ENV}")
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
                    """
            Utils.create_file_insert_data(f"{DIR_ENV}", dataToEnv)
            Utils.print_with_time(f"Created successfully: {DIR_ENV}")
        except Exception as e:
            Utils.print_with_time(f"Error creating: {DIR_ENV}: {e}")
else:
    Utils.print_with_time(f"Successfully located Env {DIR_ENV}")
simulate_loading()
folder_path = select_directories()


selenium_type = selections("\nSelected de folder you need:",['Selenoid', 'Selenium Grid'])
simulate_loading()
botName = get_value("Enter your bot's name:", onlyLetters=True)
simulate_loading()
selenium_type = "SeleniumGrid" if selenium_type == 1 else "Selenoid"
botStr = botName
script = f"""
from {selenium_type} import {selenium_type}
from core.Utils import Utils
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

    MAX_COUNT_ERRORS = 4
    ACTUAL_COUNT_ERROR = MAX_COUNT_ERRORS

    def execucao_geral(self):
        Utils.Utils.print_with_time_with_time("Inicio da execução")
        try:
            self.start_driver()
            if self.executar_login() is False:
                raise Exception("Erro ao executar o login")
        except Exception as e:
            self.ACTUAL_COUNT_ERROR -= 1
            if self.ACTUAL_COUNT_ERROR > 0:
                Utils.print_with_time(f"Erro ao iniciar o driver:{{e}} - Tentando novamente - {{self.ACTUAL_COUNT_ERROR}} / {{self.MAX_COUNT_ERRORS}}")
                return "CONTINUE"
            return "BREAK"

    def executar_login(self, MAX_COUNT_ERRORS = 3):
        try:
            driver = self.get_driver()
            if "url da aplicação" not in driver.current_url:
                if self.navigate_to_url("url da aplicação") is False:
                    raise Exception("Não foi possível acessar a página de login.")

            self.send_keys_into_element("elemento_user", self.user.cpf)
            self.send_keys_into_element("elemento_senha]", self.user.senha)
            self.click_element("elemento_entrar", By.XPATH)
            self.wait_page_loading()

            if "url da pagina de resultado" not in driver.current_url:
                Utils.Utils.print_with_time_with_time("Não foi possível acessar o login...")
                if MAX_COUNT_ERRORS > 0:
                    Utils.Utils.print_with_time_with_time("Tentando novamente")
                    return self.executar_login(MAX_COUNT_ERRORS)
                Utils.Utils.print_with_time_with_time("Desativando usuário")
                self.desativar_user("user_INVÁLIDO")
                return False

            Utils.Utils.print_with_time_with_time("Usuário logado com sucesso")
            return True
        except Exception as e:
            Utils.Utils.print_with_time_with_time(f"Erro ao executar o login: {{e}}")
            MAX_COUNT_ERRORS -= 1
            if MAX_COUNT_ERRORS > 0:
                Utils.Utils.print_with_time_with_time("Tentando realizar o login novamente")
                return self.executar_login(MAX_COUNT_ERRORS)
            Utils.Utils.print_with_time_with_time("Falha ao executar o login, finalizando.")
            return False

    def execucao_consulta(self):
        Utils.Utils.print_with_time_with_time("Iniciando a execução da consulta")

        if self.information_to_consult is None:
            self.information_to_consult = self.buscar_dados()
            if self.information_to_consult is False:
                self.information_to_consult = None
                return "CONTINUE"
        
        respostaConsulta = self.executar_consulta()

        if respostaConsulta is False:
            Utils.Utils.print_with_time_with_time("Falha ao realizar a consulta")
            if self.ACTUAL_COUNT_ERROR <= 0:
                Utils.Utils.print_with_time_with_time("Reiniciando tela")
                return "BREAK"

            self.ACTUAL_COUNT_ERROR -= 1
            Utils.Utils.print_with_time_with_time("Tentando novamente")
            return "CONTINUE"
        elif respostaConsulta == "FALHA":
            return "BREAK"
        
        return "CONTINUE"

    def executar_consulta(self, max_errors = 3):
        try:
            pass
        except Exception as e:
            Utils.Utils.print_with_time_with_time(f"Erro ao executar consulta - tentativas {{max_errors}} - {{e}}")
            if max_errors > 0:
                return self.executar_consulta(max_errors=max_errors-1)
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
