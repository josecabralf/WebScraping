from soup import getSoup
from scraperPublicacion import scrapZonaPropPublicacion
from config import URL_Base
from datetime import date
import json


def crearListaLinks(link):
    soup = getSoup(link)
    contenedor_casas = soup.find_all('div', class_ = 'sc-i1odl-0 crUUno')
    links_casas = []

    for i in range(len(contenedor_casas)):
        link = contenedor_casas[i]["data-to-posting"]
        if link:
            links_casas.append(URL_Base + link)
    return links_casas


def escribirArchivo(archivo, links_casas):
    # Último link para realizar chequeos de escritura
    ultimaCasa = links_casas[-1]
    hoy = date.today()
    with open(archivo, 'w', encoding='utf-8') as archivoJSON:
        archivoJSON.write('[')

        for link in links_casas:
            # Scrap de la publicación de la casa
            objetoJSON = scrapZonaPropPublicacion(link, hoy)

            # Chequeamos que el objeto exista (que la función haya devuelto un valor != de False)
            if objetoJSON:
                # Lo escribimos en el archivo
                json.dump(objetoJSON, archivoJSON, indent=9)
                if link != ultimaCasa:
                    # Agregamos la ',' separadora de objetos a menos que sea la última casa
                    archivoJSON.write(',')

        archivoJSON.write(']')


def scrapZonaProp(link, archivo):
    links_casas = crearListaLinks(link)
    escribirArchivo(archivo, links_casas)
