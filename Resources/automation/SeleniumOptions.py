from selenium import webdriver
import undetected_chromedriver as uc
from Resources.automation.ProxyOption import ProxyOption
from Resources.core.Utils import Utils
import os

class SeleniumOptions(ProxyOption):
    extensions = []

    experimental_options = {"excludeSwitches":["enable-automation"], 'useAutomationExtension': False}
    
    options = ["--disable-gpu", "--no-sandbox", "-disable-quic", 
            '-ignore-ssl-errors=yes', '-ignore-certificate-errors', "--disable-blink-features=AutomationControlled",
            "--disable-popup-blocking", "--disable-infobars", '--no-sandbox', '--disable-dev-shm-usage', 
            f'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0']
    
    def get_options(self):
        return self.options
    
    def add(self, option):
        self.options.append(option)
        return self
    
    def add_experimental_option(self, key, value):
        self.experimental_options[key] = value
        return self
    
    def remove_experimental_option(self, key):
        if key in self.experimental_options:
            del self.experimental_options[key]
        return self
    
    def remove(self,option):
        self.options.remove(option)
        return self
    
    def add_extension(self, extension_path):
        if not os.path.exists(extension_path):
            raise FileNotFoundError(f"Extension not found: {extension_path}")
        self.extensions.append(extension_path)
        return self
    
    def chrome_options(self):
        options = webdriver.ChromeOptions()
        for opt in self.options:
            options.add_argument(opt)

        proxy = self.get_proxy()

        if proxy is not False:
            if proxy.need_extension():
                options.add_extension(proxy.get_extension())
            else:
                options.add_argument("--disable-extensions")
                options.add_argument(f'--proxy-server={proxy.get_proxy()}')
                
        for ext_path in self.extensions:
            if ext_path.endswith('.crx'):
                options.add_extension(ext_path)
            else:
                options.add_argument(f'--load-extension={ext_path}')

        for key, value in self.experimental_options.items():
            options.add_experimental_option(key, value)

        binary_location = Utils.get_env('CHROME_BINARY_LOCATION')
        if binary_location is not None:
            options.binary_location = binary_location
        return options
    
    def undected_chrome_options(self):
        options = uc.ChromeOptions()
        self.experimental_options.pop("excludeSwitches")
        self.experimental_options.pop("useAutomationExtension")
        
        for opt in self.options:
            options.add_argument(opt)

        proxy = self.get_proxy()

        if proxy is not False:
            if proxy.need_extension():
                options.add_extension(proxy.get_extension())
            else:
                options.add_argument("--disable-extensions")
                options.add_argument(f'--proxy-server={proxy.get_proxy()}')
                
        for ext_path in self.extensions:
            if ext_path.endswith('.crx'):
                options.add_extension(ext_path)
            else:
                options.add_argument(f'--load-extension={ext_path}')

        for key, value in self.experimental_options.items():
            options.add_experimental_option(key, value)

        return options