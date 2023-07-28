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
    path = "./ZonaProp/ZP V2/driver/chromedriver"
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


def getUbicGeo(soup):
    mapa = soup.find('img', id="static-map")["src"]
    loc = mapa.split('?')[1].split('&')[0].split('=')[1]
    loc = [float(n) for n in loc.split(',')]
    return loc


url = 'https://www.zonaprop.com.ar/propiedades/venta-departamento-1-dormitorio-c-asador-nueva-cordoba-52051968.html'
soup = getSoup(url)
ubic = getUbicGeo(soup)
print(ubic)
