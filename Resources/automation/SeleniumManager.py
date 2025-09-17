import selenium.common
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.support.ui import WebDriverWait
from Resources.core.Utils import Utils
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class SeleniumManager:
    MAX_WEBDRIVER_WAIT = 2
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
        
    def scroll_into_element(self, element):
        try:
            if self.driver is not None:
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except Exception as e:
            Utils.print_with_time(f"Fail scroll into element: {e}")
            pass

    def check_loader_element(self, select = "", by = By.CSS_SELECTOR):
        if self.check_alert() is not False:
            return
        
        for i in range(10):
            try:
                element = self.select_element(select, by, True, False)
                if element is not None and element.is_displayed():
                    Utils.sleep(1)
                    continue
                break
            except:
                break
        return
    
    def check_alert(self):
        try:
            alert = self.driver.switch_to.alert
            return alert.text
        except:
            return False
    
    def send_keys_into_element(self, select = "", valueToSent = "", by = By.CSS_SELECTOR, raiseError = True):
        element = self.select_element(select, by, True, False, False)
        
        if element is None:
            if raiseError:
                raise selenium.common.NoSuchElementException(f"Element not found - {select} - {by}")
            return False
        if element.get_attribute("value") == valueToSent:
            return True
        
        if self.send_keys(element, valueToSent) is False:
            if raiseError:
                raise selenium.common.ElementNotInteractableException(f"Non-interactable element {select} - {by}")
            return False
        
    def send_keys_one_by_one(self, select = "", valueToSent = "", by = By.CSS_SELECTOR, raiseError = True):
        element = self.select_element(select, by, True, False, False)

        if element is None:
            if raiseError:
                raise selenium_exceptions.NoSuchElementException(f"Element not found - {select} - {by}")
            return False

        current_value = element.get_attribute("value")
        if current_value == valueToSent:
            return True
        
        element.clear()
        try:
            for char in valueToSent:
                element.send_keys(char)
                # time.sleep(0.05)
        except Exception as e:
            if raiseError:
                raise selenium_exceptions.ElementNotInteractableException(f"Fail digit into element {select} - {by}: {e}")
            return False

        return True
    
    def send_keys(self, element, valueToSent):
        try:
            self.driver.execute_script(f"arguments[0].focus()", element)
            Utils.sleep(0.5)
            self.driver.execute_script(f"arguments[0].value = '{valueToSent}';", element)
            Utils.sleep(0.5)
            self.driver.execute_script(f"arguments[0].blur()", element)
            return True
        except (selenium.common.InvalidElementStateException, selenium.common.StaleElementReferenceException):
            try:
                self.driver.execute_script(f"arguments[0].value = '{valueToSent}';", element)
            except Exception as e:
                Utils.print_with_time(f"Error send key into element - {element} - {valueToSent}: {e}")
                return False
    
    def click_element(self, select = "", by = By.CSS_SELECTOR, raiseError = True):
        element = self.select_element(select, by, True, False, False)
        
        if element is None:
            if raiseError:
                raise selenium.common.NoSuchElementException(f"Element not found - {select} - {by}")
            return False
                
        if self.click(element) is False:
            if raiseError:
                raise selenium.common.ElementNotInteractableException(f"Non-interactable element {select} - {by}")
            return False
        return True
    
    def click(self, element):
        try:
            self.driver.execute_script(f"arguments[0].click()", element)
            Utils.sleep(0.5)
            return True
        except (selenium.common.InvalidElementStateException, selenium.common.StaleElementReferenceException):
            try:
                self.driver.execute_script(f"arguments[0].click();", element)
            except:
                return False
    
    def hover_element(self, select: str, by=By.CSS_SELECTOR, raiseError=True):
        try:
            element = self.select_element(select, by, scrollInto=True, raiseError=raiseError)
            if element:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()
                Utils.sleep(3)
                return True
            else:
                if raiseError:
                    raise selenium.common.NoSuchElementException(f"Element not found to hover - {select} - {by}")
                return False
        except Exception as e:
            if raiseError:
                raise selenium.common.ElementNotInteractableException(f"Error into hover to element - {select} - {by} - {e}")
            return False
            
    @staticmethod
    def wait_page_loading_(driver, MAX_WEBDRIVER_WAIT = None):
        try:

            if MAX_WEBDRIVER_WAIT is None:
                WebDriverWait(driver, SeleniumManager.MAX_WEBDRIVER_WAIT).until(lambda driver: driver.execute_script("return window.xmlHttpRequest.active === 0"))
            else:
                WebDriverWait(driver, MAX_WEBDRIVER_WAIT).until(lambda driver: driver.execute_script("return window.xmlHttpRequest.active === 0"))
        except:
            if MAX_WEBDRIVER_WAIT is None:
                WebDriverWait(driver, SeleniumManager.MAX_WEBDRIVER_WAIT).until(lambda driver: driver.execute_script("return window.activeAjaxRequests === 0"))
            else:
                WebDriverWait(driver, MAX_WEBDRIVER_WAIT).until(lambda driver: driver.execute_script("return window.activeAjaxRequests === 0"))
    
    def wait_page_loading(self):
        try:
            driver = self.driver
            SeleniumManager.wait_page_loading_(driver, self.MAX_WEBDRIVER_WAIT)
        except:
            pass
        
    @staticmethod
    def go_to_url_(driver, url):
        driver.get(url)
        Utils.sleep(0.5)

    def go_to_url(self, url):
        SeleniumManager.go_to_url_(self.driver, url)
            