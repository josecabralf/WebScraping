from bs4 import BeautifulSoup
import requests
from scraperPublicacion import scrapLaVozPublicacion
import json


def crearListaLinks(URL):
    """Crea una lista de links de publicaciones a scrapear a partir de una URL que posee nos conduce a un listado de publicaciones.

    Args:
        URL (string): URL que nos conduce al listado de publicaciones

    Returns:
        [string]: listado de links de publicaciones individuales
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    pagina_casas = soup.find_all('a', class_="text-decoration-none")

    links_casas = set()
    for link in pagina_casas:
        links_casas.add(link["href"])

    return list(links_casas)


def escribirArchivo(archivo, links_casas):
    """Esta funcion nos permite recorrer uno por uno un arreglo de links que nos conducen a publicaciones de casas individuales para poder scrapear datos sobre ellas y escribir dichos datos en un archivo json.

    Args:
        archivo (string): define el nombre y ruta del archivo json que se quiere generar a partir de los datos scrapeados. Ej. './Casas/pagina1.json'
        links_casas ([string]): arreglo con la lista de links de casas que se quieren scrapear
    """
    ultimaCasa = links_casas[-1]

    with open(archivo, 'w', encoding='utf-8') as archivoJSON:
        archivoJSON.write('[')

        for link in links_casas:
            objetoJSON = scrapLaVozPublicacion(link)

            if objetoJSON:
                json.dump(objetoJSON, archivoJSON, indent=9)
                if link != ultimaCasa:
                    archivoJSON.write(',')

        archivoJSON.write(']')


def scrapLaVozClasificados(URL, archivo):
    """Esta funcion nos permite scrapear datos de una pagina web que posee un listado de publicaciones; y escribe dichos datos en un archivo

    Args:
        URL (string): URL que nos conduce al listado de publicaciones
        archivo (string): define el nombre y ruta del archivo json que se quiere generar a partir de los datos scrapeados. Ej. './Casas/pagina1.json'
    """
    links_casas = crearListaLinks(URL)
    escribirArchivo(archivo, links_casas)
