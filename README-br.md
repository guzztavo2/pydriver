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