from bs4 import BeautifulSoup
import requests
from scraperPublicacion import scrapMeLiPublicacion
import json
from datetime import date


def crearListaLinks(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = [link["href"] for link in soup.find_all('a', class_ = 'ui-search-item__group__element shops__items-group-details ui-search-link')]
    return links

def escribirArchivo(archivo, links_casas):
    ultimaCasa = links_casas[-1]  # Último link para realizar chequeos después
    hoy = date.today()
    with open(archivo, 'w', encoding='utf-8') as archivoJSON:
        archivoJSON.write('[')

        for link in links_casas:
            # Scrap de la publicación de la casa
            objetoJSON = scrapMeLiPublicacion(link, hoy)

            # Chequeamos que el objeto exista (que la función haya devuelto un valor != de False)
            if objetoJSON:
                # Lo escribimos en el archivo
                json.dump(objetoJSON, archivoJSON, indent=9)
                if link != ultimaCasa:
                    # Agregamos la ',' separadora de objetos a menos que sea la última casa
                    archivoJSON.write(',')

        archivoJSON.write(']')


def scrapMeLi(URL, archivo):
    links_casas = crearListaLinks(URL)
    escribirArchivo(archivo, links_casas)
