from scraperPublicacion import scrapZonaPropPublicacion
from config import URL_Base
import json


def crearListaLinks(driver):

    contenedor_casas = driver.find_elements_by_xpath(
        '//div[@class = "postings-container"]/div/div')
    links_casas = []

    for i in range(len(contenedor_casas)):
        link = contenedor_casas[i].get_attribute("data-to-posting")
        if link:
            links_casas.append(URL_Base + link)

    return links_casas


def escribirArchivo(archivo, links_casas):
    # Último link para realizar chequeos de escritura
    ultimaCasa = links_casas[-1]

    with open(archivo, 'w', encoding='utf-8') as archivoJSON:
        archivoJSON.write('[')

        for link in links_casas:
            # Scrap de la publicación de la casa
            objetoJSON = scrapZonaPropPublicacion(link)

            # Chequeamos que el objeto exista (que la función haya devuelto un valor != de False)
            if objetoJSON:
                # Lo escribimos en el archivo
                json.dump(objetoJSON, archivoJSON, indent=9)
                if link != ultimaCasa:
                    # Agregamos la ',' separadora de objetos a menos que sea la última casa
                    archivoJSON.write(',')

        archivoJSON.write(']')


def scrapZonaProp(driver, archivo):
    links_casas = crearListaLinks(driver)
    escribirArchivo(archivo, links_casas)
