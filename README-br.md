# PyDriver

PyDriver é um framework criado para facilitar o uso do **Selenium** em Python, 
tanto em ambientes de desenvolvimento com **Selenium Grid** ou **Selenoid**, quanto em produção.

Ele oferece:
- 🚀 Facilidade de uso  
- 📦 Portabilidade  
- 🔒 Isolamento via **Docker**  
- 👀 Visualização via **VNC** (opcional em ambiente de desenvolvimento)  

---

## 📋 Pré-requisitos

Você não precisa instalar o **Python** localmente, pois ele já vem no pacote do **Dockerfile**.

O Dockerfile já contém:  
- Python 3.8  
- Chromium + Chromium Driver  
- Xvfb, Fluxbox e TigerVNC (para visualização do navegador em Dev)  
- Dependências gráficas necessárias para o Selenium rodar corretamente  

---

## ⚙️ Instalação

Clone o repositório e suba o container:

```bash
docker compose build --no-cache
docker compose up -d
```

Ou, no VSCode, instale a extensão **Dev Containers** e rode:  
```
Dev Containers: Build and Open in Container
```

---

## 🖥️ Acesso ao VNC

Para visualizar o navegador (modo Dev), utilize um cliente **VNC**.

### Linux
```bash
sudo apt-get install tigervnc-viewer
vncviewer localhost:5901
```

### Windows
Baixe e instale o [RealVNC Viewer](https://www.realvnc.com/).  
Depois conecte em:  
```
localhost:5901
```

---

## 📂 Estrutura do Projeto

```
/Resources
  /automation/
    Proxy.py
    ProxyOption.py
    SeleniumDriver.py
    SeleniumManager.py
    SeleniumOptions.py
  /core/
    Loop.py
    Utils.py
  /integrations/
    Api.py
    ApiUser.py
    MySql.py
    MySqlConnection.py
  .env
  CreateNewBot.py
  SeleniumGrid.py
  Selenoid.py
```

---

## ⚡ Uso do Framework

1. Execute o script `CreateNewBot.py` para criar um novo bot:
   ```bash
   python Resources/CreateNewBot.py
   ```
   Ele pedirá o nome do script e o driver (Selenium Grid ou Selenoid).

2. Configure o arquivo `.env` conforme necessário:

   ```env
   START_IN_PRODUCTION = False
   API_URL = "http://sua-api.com"
   SELENIUMGRID_URL = "http://grid:4444/wd/hub"
   SELENOID_URL = "http://selenoid:4444/wd/hub"
   MYSQL_IN_PRODUCTION = False
   MYSQL_TEST = "mysql://root:senha@localhost/testdb"
   MYSQL_PRODUCTION = "mysql://root:senha@prod-db/proddb"
   CHROME_BINARY_LOCATION = "/usr/bin/chromium"
   ```

3. Execute seu bot criado!

---

## 🛠️ Funcionalidades Principais

- **Gerenciamento do SeleniumDriver**
  - `start_driver`, `quit_driver`, etc.  
- **Gerenciamento de Elementos**
  - `select_element`, `send_keys_into_element`, `click_element`, etc.  
- **Proxy Management**
  - `add_proxy`, `array_to_proxies`  
- **Integrações**
  - MySQL (busca, inserção e queries)  
  - API (requisições e respostas preparadas)  
- **Funções auxiliares (`Utils`)**
  - `print_with_time`, `validate_cpf`, `only_numbers`, `request_and_prepare_response`, etc.  

---

## 🧩 Customizações

Você pode sobrescrever funções em seu próprio script.  
Exemplo: redefinindo `select_element` para usar **Expected Conditions**:

Essa versão é a mais rapida, já que usa o `find_element's` para buscar os elementos, o problema é que pode dar problema em certas páginas, então caso você tenha mais de robô, essa mudança é interessante, que você pode modificar qualquer função:
```python - find_element
def select_element(self, select, by = By.XPATH, scrollInto = True, isMultipleElements = False, raiseError = True, parentElement = None):
        try:
            self.driver.implicitly_wait(2)
            element_s = None
            if isMultipleElements:
                if parentElement is not None:
                    element_s = parentElement.find_elements(by, select)
                else:
                    element_s = self.driver.find_elements(by, select)
                if scrollInto:
                    self.scroll_into_element(element_s[0])
            else:
                if parentElement is not None:
                    element_s = parentElement.find_element(by, select)
                else:
                    element_s = self.driver.find_element(by, select)
                if scrollInto:
                    self.scroll_into_element(element_s)
                    
            if Utils.is_empty(element_s):
                if raiseError:
                    raise selenium.common.ElementNotInteractableException(f"Non-interactable element - {select} - {by}")
            
            return element_s
            
        except selenium.common.NoSuchElementException:
            if raiseError:
                raise selenium.common.NoSuchElementException(f"Non-interactable element - {select} - {by}")
            return None
        except Exception as e:
            Utils.print_with_time(f"Erro ao buscar elemento: {e}")
            if raiseError:
                raise selenium.common.NoSuchElementException(f"Non-interactable element - {select} - {by}")
            Utils.print_with_time(f"Non-interactable element - {select} - {by}")
            return None
```

```python - Expected Conditions
def select_element(self, select, by = By.XPATH, scrollInto=True, isMultipleElements=False, raiseError=True, parentElement=None):
    try:
        wait = WebDriverWait(self.driver, self.MAX_WEBDRIVER_WAIT)
        if isMultipleElements:
            element_s = wait.until(EC.presence_of_all_elements_located((by, select)))
        else:
            element_s = wait.until(EC.presence_of_element_located((by, select)))
        return element_s
    except Exception as e:
        Utils.print_with_time(f"Erro ao buscar elemento: {e}")
        return None
```

## Você pode encontrar um exemplo de bot:
```
bot_test.py
from Resources.SeleniumGrid import SeleniumGrid
from Resources.core.Utils import Utils
from selenium.webdriver.common.by import By
from Resources.automation.ProxyOption import ProxyOption

def auto_run(cls):
    instance = cls()  
    instance.start_thread()
    return cls

@auto_run
class test(SeleniumGrid):
    session_name = "BOT_TEST"
    consult_table_name = ""
    result_table_name = ""
    information_to_consult = None

    TARGET_URL = ""
    MAX_COUNT_ERRORS = 4
    ACTUAL_COUNT_ERROR = MAX_COUNT_ERRORS

    def start_proxies():
        proxyIpList = ["ip1", "ip2"]
        proxyPortList = ["port1", "port2"]
        proxyUsernameList = ["user1", "user2"]
        proxyPasswordList = ["pass1", "pass2"]
        ProxyOption.array_to_proxies(proxyIpList, proxyPortList, proxyUsernameList, proxyPasswordList)

    def general_execution(self):
        Utils.print_with_time(f"Starting General Execution - {self.GeneralExecution.current_position}")
        try:
            if self.GeneralExecution.is_first():
                self.options.add('--remote-debugging-port=9222')
                # self.start_proxies()
            self.start_driver(page_load_strategy='none', load_images = False, use_undected_chrome_driver = False) 
            if self.execute_login() is False:
                raise Exception("Error in execution of login")
        except Exception as e:
            self.ACTUAL_COUNT_ERROR -= 1
            if self.ACTUAL_COUNT_ERROR > 0:
                Utils.print_with_time(f"Error in starting driver:{e} - Trying againg - {self.ACTUAL_COUNT_ERROR} / {self.MAX_COUNT_ERRORS}")
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
            Utils.print_with_time(f"Error in execute login: {e}")
            max_login_errors -= 1

            if max_login_errors > 0:
                Utils.print_with_time("Trying execute login again")
                return self.execute_login(max_login_errors)
            Utils.print_with_time("Fail in execute login, finalizing.")
            return False

    def consult_execution(self):
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
            Utils.print_with_time(f"Error in execution of consult - attempts {max_errors} - {e}")
            if max_errors > 0:
                return self.execute_consult(max_errors=max_errors-1)
            return False
```
