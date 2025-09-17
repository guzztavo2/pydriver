from abc import abstractmethod
from Resources.automation.SeleniumManager import SeleniumManager
from Resources.automation.SeleniumOptions import SeleniumOptions
from Resources.core.Utils import Utils

class SeleniumDriver(SeleniumManager):
    
    driver = None
    start_in_production = True if Utils.get_env('START_IN_PRODUCTION') == 'True' else False
    options = None
    
    def __init__(self, options = None):
        self.set_options(options)

    @classmethod
    def set_startInProduction(cls, start_in_production):
        cls.start_in_production = start_in_production

    @classmethod
    def set_options(cls,options):
        options_ = None
        if options is None or isinstance(options, SeleniumOptions) is False:
            if cls.options is not None:
                options_ = cls.options
                cls.options = SeleniumOptions()
                cls.options.options = options_
            else:
                cls.options = SeleniumOptions()
        else:
            cls.options = options

    @classmethod 
    def add_option(cls, option):
        cls.options.add(option)
        return cls
    
    @classmethod 
    def remove_option(cls, option):
        cls.options.remove(option)
        return cls
    
    @classmethod 
    def add_extension(cls, extension_path):
        if cls.options is None:
            cls.options = SeleniumOptions()
        cls.options.add_extension(extension_path)
        return cls
    
    @classmethod 
    def restart_driver(cls, session_name = '', page_load_strategy='none', loadImage = True):
        cls.quit_driver()
        return cls.start_driver(session_name, page_load_strategy, loadImage)
    
    @classmethod
    def get_driver(cls):
        return cls.driver
    
    @classmethod
    def update_driver(cls, driver):
        cls.driver = driver

    @classmethod
    def get_options(cls):
        return cls.options
    
    @classmethod
    def quit_driver(cls):
        try:
            driver = cls.get_driver()
            if driver is not None:
                windowList = driver.window_handles
                for window in windowList:
                    driver.switch_to.window(window)
                    driver.close()
                    Utils.sleep(0.2)
        finally:
                if driver is not None:
                    driver.stop_client()
                    driver.quit()
                cls.update_driver(None)

    @abstractmethod
    def start_driver(cls, session_name = '', page_load_strategy='none', loadImage = True):
        pass

    @classmethod
    def navigate_to_url(cls,url):
        cls.go_to_url_(cls.driver,url)
        cls.driver.implicitly_wait(cls.MAX_WEBDRIVER_WAIT)
        cls.wait_page_loading(cls)
        
        if url not in cls.driver.current_url:
            Utils.print_with_time(f"Failed to access url: {url}")
            return False
        Utils.print_with_time(f"Successful to access url: {url}")
        return True
    