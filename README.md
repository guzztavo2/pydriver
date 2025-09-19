# Pydriver

**Pydriver** is a framework designed to simplify the use of Selenium drivers in Python, with support for both development environments (using VNC/Docker) and production environments (Selenium Grid or Selenoid).

The framework focuses on:
- **Ease of use**
- **Portability**
- **Isolation**

It runs inside Docker containers, and for development, it uses **VNC** for browser visualization. In **production**, VNC is not required, but the necessary packages must still be present.

---

## 📦 Installation

Clone the repository and start the containers:

```bash
docker compose build --no-cache
docker compose up
```

For **VSCode**, use the **Dev Containers** extension:

```
Dev Containers: build and open in container
```

### Browser visualization (optional)

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt-get install tigervnc-viewer
  vncviewer localhost:5901
  ```

- **Windows:**
  Download [RealVNC Viewer](https://www.realvnc.com/)
  ```
  Connect to: http://localhost:5901
  ```

---

## ⚙️ Project Structure

```bash
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

### Main Directories

- **automation/** → Selenium drivers and configuration.
- **core/** → Utility functions and execution loops.
- **integrations/** → Ready-to-use integrations (MySQL, API, etc.).

---

## 🚀 Creating a new bot

The first script to run is **CreateNewBot.py**:

```bash
python Resources/CreateNewBot.py
```

This will:
- Create a new script with the chosen name and driver (Selenium Grid or Selenoid).
- Validate and configure environment variables (.env).
- Suggest the best path to place your script.

⚠️ **Recommendation:** keep your scripts at least **one directory above `./Resources/`**.

Example imports depending on the directory structure:
```python
# Script at the same level as Resources
from automation.SeleniumDriver import SeleniumDriver

# Script one level above Resources
from Resources.automation.SeleniumDriver import SeleniumDriver

# Script two levels above
from pydriver.Resources.automation.SeleniumDriver import SeleniumDriver
```

---

## 🔧 Environment Variables (.env)

| Variable                 | Description |
|---------------------------|-------------|
| `START_IN_PRODUCTION`     | `True` or `False`. Runs in production (Grid/Selenoid) or development. |
| `API_URL`                 | API URL used for integrations. |
| `SELENIUMGRID_URL`        | URL of Selenium Grid when running in production. |
| `SELENOID_URL`            | URL of Selenoid when running in production. |
| `MYSQL_IN_PRODUCTION`     | `True` or `False`. Selects between `MYSQL_PRODUCTION` or `MYSQL_TEST`. |
| `CHROME_BINARY_LOCATION`  | Path to Chrome binary (if needed). |

---

## 🧩 Key Components

### automation/
- **SeleniumOptions.py** → Selenium options configuration (user agents, experimental options, etc.).
- **ProxyOption.py** → Proxy management:
  - `add_proxy(proxy)` → add a proxy.
  - `array_to_proxies(list)` → add multiple proxies (with/without authentication).
- **SeleniumManager.py** → Interaction with web elements:
  - `select_element`
  - `scroll_into_element`
  - `send_keys`
  - `click_element`
  - and more.
- **SeleniumDriver.py** → Driver management (start, quit, production/dev mode).

### core/
- **Utils.py** → Utility functions:
  - `print_with_time`, `request_and_prepare_response`, `url_encoded`, `validate_cpf`, `only_numbers`, etc.
- **Loop.py** → Execution loop management (`general_execution`, `consult_execution`).

### integrations/
- **Api.py / ApiUser.py** → API requests.
- **MySql.py / MySqlConnection.py** → MySQL database integrations.

You can easily add new integrations and import them into `Resources/Selenoid.py` or `Resources/SeleniumGrid.py`.

---

## 🛠️ Features

- **Proxy** support (with and without authentication).
- Custom **User Agents**.
- **Undetected ChromeDriver** to bypass bot detection.
- API and **MySQL integrations**.
- **Development mode** (with VNC) and **Production mode** (Grid/Selenoid).

---

## 📄 Dependencies

All dependencies are listed in:
```
./requirements.txt
```

---

## 📌 Conclusion

**Pydriver** was created to simplify Selenium usage in isolated Docker environments, reducing complexity and providing flexibility for both development and production.

---

