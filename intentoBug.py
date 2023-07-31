from bs4 import BeautifulSoup
import requests

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from time import sleep


def getSoup(link):
    """Crea un objeto BeautifulSoup a partir de un link de una página web dinámica.

    Args:
        link (string): url de la página dinámica

    Returns:
        BeautifulSoup: contenidos de la página web
    """
    path_driver = 'ZonaProp\ZP V3\driver\chromedriver'
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
        soup = getSoup(link)
    return soup


def getTipoVendedor(soup):
    vendedor = soup.find('div', class_='feature-info')
    if vendedor:
        return 'PARTICULAR'
    return 'INMOBILIARIA'


url = 'https://www.zonaprop.com.ar/propiedades/casa-en-venta-belgrano-r-av-de-los-incas-52061318.html'
s = getSoup(url)
v = getTipoVendedor(s)
print(v)
