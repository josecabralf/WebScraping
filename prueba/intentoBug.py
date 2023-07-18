from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from datetime import date, timedelta

def getSoup(link):
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = Chrome(options=options)
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup

def getFecha(soup, hoy):
    """Obtiene la fecha de publicación/última actualización de una publicación de ZP

    Args:
        soup (BeautifulSoup): objeto BeautifulSoup con los datos de la publicacion
        hoy (date): fecha del día de la fecha para calcular la fecha de publicación/última actualización

    Returns:
        Case 1 date: fecha de publicación/última actualización (dd-mm-yy)
        Case 2 bool: False para indicar que no se pudo encontrar
    """
    try:
        delta = soup.find('div', id='user-views').find('p').text.split()
        if delta[-1] in ['día', 'días']:
            delta = int(delta[-2])
        elif delta[-1] in ['mes', 'meses']:
            delta = 31*int(delta[-2])
        elif delta[-1] in ['año', 'años']:
            delta = 365*int(delta[-2])
        
        fecha = hoy - timedelta(days=delta)
        fecha = fecha.strftime("%d-%m-%Y")
        return fecha
    except:
        return False

URL = "https://www.zonaprop.com.ar/propiedades/depto-nva-cba-oportunidad!-51758184.html"

soup = getSoup(URL)
fecha = getFecha(soup, date.today())
print(fecha)