from abc import abstractmethod
import requests
from bs4 import BeautifulSoup
from config import path_driver
from selenium.webdriver import Chrome, ChromeOptions
from src.Singleton import Singleton


class SoupStrategy(Singleton):
    @abstractmethod
    def execute(self, url) -> BeautifulSoup: ...


class Requests(SoupStrategy):
    def execute(self,url) -> BeautifulSoup:
        res = requests.get(url)
        return BeautifulSoup(res.content, 'html.parser')
    

class Selenium(SoupStrategy):
    def __init__(self) -> None:
        super().__init__()
        self._path_driver = path_driver
        self.set_options()
        
    def execute(self,url) -> BeautifulSoup:
        driver = self.get_driver()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup

    def set_options(self):
        self._options = ChromeOptions()
        self._options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self._options.add_argument("--headless")
        self._options.add_argument('--blink-settings=imagesEnabled=false')
        self._options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        
    def get_driver(self):
        try: driver = Chrome(executable_path=self._path_driver, options=self._options)
        except: driver = Chrome(options=self._options)
        return driver