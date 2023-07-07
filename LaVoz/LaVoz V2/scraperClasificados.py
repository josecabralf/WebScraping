from bs4 import BeautifulSoup
import requests
from scraperPublicacion import scrapLaVozPublicacion
import json

def crearListaLinks(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    pagina_casas = soup.find_all('a', class_="text-decoration-none") # Obtenemos todas las casas de la página
    
    links_casas = set()
    for link in pagina_casas:
        links_casas.add(link["href"])

    return list(links_casas)


def escribirArchivo(archivo, links_casas):
    ultimaCasa = links_casas[-1] # Último link para realizar chequeos después

    with open(archivo, 'w', encoding='utf-8') as archivoJSON:
        archivoJSON.write('[')
        
        for casa in links_casas:
            objetoJSON = scrapLaVozPublicacion(casa) # Scrap de la publicación de la casa

            if objetoJSON: # Chequeamos que el objeto exista (que la función haya devuelto un valor != de False)
                json.dump(objetoJSON, archivoJSON, indent=9) # Lo escribimos en el archivo
                if casa != ultimaCasa:
                    archivoJSON.write(',') # Agregamos la ',' separadora de objetos a menos que sea la última casa
        
        archivoJSON.write(']')


def scrapLaVozClasificados(URL,archivo):
    links_casas = crearListaLinks(URL)
    escribirArchivo(archivo, links_casas)