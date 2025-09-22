# PyDriver

PyDriver is a framework created to facilitate the use of **Selenium** in Python, both in development environments with **Selenium Grid** or **Selenoid**, and in production.

It offers:
- 🚀 Ease of use
- 📦 Portability
- 🔒 Isolation via **Docker**
- 👀 Viewing via **VNC** (optional in development environment)

---

## 📋 Prerequisites

You don't need to install **Python** locally, as it is already packaged in the **Dockerfile**.

The Dockerfile already contains:
- Python 3.8
- Chromium + Chromium Driver
- Xvfb, Fluxbox, and TigerVNC (for browser viewing in Dev)
- Graphical dependencies required for Selenium to run correctly

---

## ⚙️ Installation

Clone the repository and run the container:

```bash
docker compose build --no-cache
docker compose up -d
```

Or, in VSCode, install the **Dev Containers** extension and run:  
```
Dev Containers: Build and Open in Container
```

---

## 🖥️ Access on VNC

To view the browser (Dev mode), use a **VNC** client.

### Linux
```bash
sudo apt-get install tigervnc-viewer
vncviewer localhost:5901
```

### Windows
Download and install [RealVNC Viewer](https://www.realvnc.com/).  
Connect in:  
```
localhost:5901
```

---

## 📂 Project structure

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

## ⚡ Using the Framework

1. Execute the script `CreateNewBot.py` to create a new bot:
   ```bash
   python Resources/CreateNewBot.py
   ```
   It will ask for the script name and driver (Selenium Grid or Selenoid).

2. Configure the archive `.env` as needed:

   ```env
    START_IN_PRODUCTION = False
    API_URL = "http://your-api.com"
    SELENIUMGRID_URL = "http://grid:4444/wd/hub"
    SELENOID_URL = "http://selenoid:4444/wd/hub"
    MYSQL_HOST_TEST=127.0.0.1
    MYSQL_USER_TEST=
    MYSQL_PASSWORD_TEST=
    MYSQL_DATABASE_TEST=

    MYSQL_HOST_PRODUCTION=
    MYSQL_USER_PRODUCTION=
    MYSQL_PASSWORD_PRODUCTION=
    MYSQL_DATABASE_PRODUCTION=
   ```

3. Run your created bot!

---

## 🛠️ Main Features

- **SeleniumDriver Management**
  - `start_driver`, `quit_driver`, etc.  
- **Element Management**
  - `select_element`, `send_keys_into_element`, `click_element`, etc.  
- **Proxy Management**
  - `add_proxy`, `array_to_proxies`  
- **Integrations**
  - MySQL (search, insertion and queries)  
  - API (prepared requests and responses)  
- **Auxiliary functions(`Utils`)**
  - `print_with_time`, `validate_cpf`, `only_numbers`, `request_and_prepare_response`, etc.  

---

## 🧩 Customizations

You can override functions in your own script.
Example: redefining `select_element` to use **Expected Conditions**:

This version is the fastest, since it uses `find_element's` to search for elements, the problem is that it can cause problems on certain pages, so if you have more than one robot, this change is interesting, as you can modify any function:
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