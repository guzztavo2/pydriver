# Pydriver

O **Pydriver** é um framework criado para facilitar o uso de drivers Selenium em Python, com suporte tanto para ambientes de desenvolvimento (usando VNC/Docker) quanto para produção (Selenium Grid ou Selenoid).

Seu foco é:
- **Facilidade de uso**
- **Portabilidade**
- **Isolamento**

Ele funciona em containers Docker, e no ambiente de desenvolvimento utiliza **VNC** para visualização do navegador. Já em **produção**, o VNC não é necessário, mas os pacotes continuam sendo obrigatórios.

---

## 📦 Instalação

Clone o repositório e rode os containers:

```bash
docker compose build --no-cache
docker compose up
```

Para abrir no **VSCode**, utilize a extensão **Dev Containers**:

```
Dev Containers: build and open in container
```

### Visualizando o navegador (opcional)

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt-get install tigervnc-viewer
  vncviewer localhost:5901
  ```

- **Windows:**
  Baixe o [RealVNC Viewer](https://www.realvnc.com/)
  ```
  Conectar em: http://localhost:5901
  ```

---

## ⚙️ Estrutura do Projeto

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

### Pastas Principais

- **automation/** → Configurações e drivers Selenium.
- **core/** → Funções utilitárias e loops de execução.
- **integrations/** → Integrações já prontas (MySQL, API, etc.).

---

## 🚀 Criando um novo bot

A primeira execução deve ser do script **CreateNewBot.py**:

```bash
python Resources/CreateNewBot.py
```

Ele irá:
- Criar um novo script com o nome e driver escolhidos (Selenium Grid ou Selenoid).
- Validar e configurar variáveis de ambiente (.env).
- Sugerir o melhor diretório para salvar seu script.

⚠️ **Recomendação:** mantenha seus scripts pelo menos **um diretório acima da pasta `./Resources/`**.

Exemplo de imports dependendo da estrutura:
```python
# Script no mesmo nível da pasta Resources
from automation.SeleniumDriver import SeleniumDriver

# Script um nível acima da Resources
from Resources.automation.SeleniumDriver import SeleniumDriver

# Script dois níveis acima
from pydriver.Resources.automation.SeleniumDriver import SeleniumDriver
```

---

## 🔧 Variáveis de Ambiente (.env)

| Variável                | Descrição |
|--------------------------|-----------|
| `START_IN_PRODUCTION`    | `True` ou `False`. Define se rodará em produção (Grid/Selenoid) ou dev. |
| `API_URL`                | URL da API usada para integrações. |
| `SELENIUMGRID_URL`       | URL do Selenium Grid quando em produção. |
| `SELENOID_URL`           | URL do Selenoid quando em produção. |
| `MYSQL_IN_PRODUCTION`    | `True` ou `False`. Define se usará `MYSQL_PRODUCTION` ou `MYSQL_TEST`. |
| `CHROME_BINARY_LOCATION` | Caminho do binário do Chrome (caso necessário). |

---

## 🧩 Componentes Principais

### automation/
- **SeleniumOptions.py** → Configurações de opções do Selenium (user agents, experimental options, etc.).
- **ProxyOption.py** → Gerenciamento de proxies:
  - `add_proxy(proxy)` → adiciona um proxy.
  - `array_to_proxies(list)` → adiciona múltiplos proxies (com ou sem autenticação).
- **SeleniumManager.py** → Interação com elementos da página:
  - `select_element`
  - `scroll_into_element`
  - `send_keys`
  - `click_element`
  - entre outros.
- **SeleniumDriver.py** → Gerenciamento do driver (start, quit, modo produção/dev).

### core/
- **Utils.py** → Funções utilitárias:
  - `print_with_time`, `request_and_prepare_response`, `url_encoded`, `validate_cpf`, `only_numbers`, etc.
- **Loop.py** → Gerenciamento de loops de execução (`general_execution`, `consult_execution`).

### integrations/
- **Api.py / ApiUser.py** → Requisições para APIs.
- **MySql.py / MySqlConnection.py** → Integrações com banco de dados MySQL.

Você pode adicionar novas integrações e importá-las em `Resources/Selenoid.py` ou `Resources/SeleniumGrid.py`.

---

## 🛠️ Recursos

- Suporte a **proxies** (com e sem autenticação).
- **User Agents** customizados.
- **Undetected ChromeDriver** para burlar detecções de robôs.
- Integrações com **APIs** e **MySQL**.
- Modo **desenvolvimento** (com VNC) e **produção** (Grid/Selenoid).

---

## 📄 Dependências

Todas as dependências estão listadas em:
```
./requirements.txt
```

---

## 📌 Conclusão

O **Pydriver** foi criado para simplificar o uso do Selenium em ambientes isolados com Docker, reduzindo complexidade e oferecendo flexibilidade para desenvolvimento e produção.

---