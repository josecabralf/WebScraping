from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from ScrapConfig import path_driver
from selenium.webdriver import Chrome, ChromeOptions


class SoupStrategy(ABC):
    _instance = None
    @abstractmethod
    def execute(self, url) -> BeautifulSoup:
        pass
    @classmethod
    def get_instance(self):
        if self._instance is None:
            self._instance = self()
        return self._instance


class SoupStrategyRequests(SoupStrategy):
    def execute(self,url) -> BeautifulSoup:
        res = requests.get(url)
        return BeautifulSoup(res.content, 'html.parser')
    

class SoupStrategySelenium(SoupStrategy):
    _path_driver = path_driver
    def execute(self,url) -> BeautifulSoup:
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try: driver = Chrome(executable_path=self._path_driver, options=options)
        except: driver = Chrome(options=options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup