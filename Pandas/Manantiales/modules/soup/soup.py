from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import requests
from time import sleep
from config import path_driver


def getDynamicSoup(link):
    """Crea un objeto BeautifulSoup a partir de un link de una página web dinámica.

    Args:
        link (string): url de la página dinámica

    Returns:
        BeautifulSoup: contenidos de la página web
    """
    try:
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = Chrome(executable_path=path_driver, options=options)
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
    except:
        sleep(5)
        soup = getDynamicSoup(link)
    return soup


def getStaticSoup(link):
    """Genera un objeto BeautifulSoup a partir de una URL de un sitio web estático.

    Args:
        link (sring): url del sitio web

    Returns:
        BeautifulSoup: objeto BeautifulSoup del sitio web
    """
    res = requests.get(link)
    return BeautifulSoup(res.content, 'html.parser')
