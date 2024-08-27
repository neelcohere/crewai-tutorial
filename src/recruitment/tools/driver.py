# ../src/project/tools/driver.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from typing import Optional, Dict


class Driver:
    def __init__(self, url: str, cookie: Optional[Dict]=None) -> None:
        self.driver = self._create_driver(url, cookie)
    
    def navigate(self, url: str, wait: int=3) -> None:
        self.driver.get(url)
        time.sleep(wait)
    
    def scroll_to_bottom(self, wait: int=3) -> None:
        self.driver.execute_script(
            "window.scrollto(0, document.body.scrollHeight);"
        )
        time.sleep(wait)
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(wait)
    
    def get_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)
    
    def get_elements(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def fill_text_field(self, selector, text: str) -> None:
        element = self.get_element(selector)
        element.clear()
        element.send_keys(text)
    
    def click_button(self, selector) -> None:
        element = self.get_element(selector)
        element.click()

    def _create_driver(self, url: str, cookies) -> webdriver.Firefox:
        options = Options()
        # options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url=url)
        if cookies:
            driver.add_cookie(cookies)
        return driver
    
    def close(self) -> None:
        self.driver.close()
