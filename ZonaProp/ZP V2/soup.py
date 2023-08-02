from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from time import sleep
from ZPConfig import path_driver as path


def getSoup(link):
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
        driver = Chrome(executable_path=path, options=options)
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
    except:
        sleep(5)
        soup = getSoup(link)
    return soup
