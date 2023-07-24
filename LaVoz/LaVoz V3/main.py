from bs4 import BeautifulSoup
import requests
from links import formarLink
from LVConfig import URL_LaVoz, archivos_LaVoz
from archivos import *
from hilos import scrapMultiHilo


def main():
    response = requests.get(URL_LaVoz)
    soup = BeautifulSoup(response.content, 'html.parser')

    paginas = int((soup.find_all('a', class_="page-link h4"))[-1].text)
    nro = asignarValNro(archivos_LaVoz)
    for i in range(1, paginas-1, 3):
        URLs = [formarLink(URL_LaVoz, n) for n in range(i, i+3)]
        archivos = [formarArchivo(n, archivos_LaVoz)
                    for n in range(nro, nro+3)]
        nro += 3
        scrapMultiHilo(URLs, archivos)

    if paginas % 3 == 1:
        scrapMultiHilo(
            [formarLink(URL_LaVoz, paginas)], [formarArchivo(paginas, archivos_LaVoz)])

    elif paginas % 3 == 2:
        URLs = [formarLink(URL_LaVoz, i) for i in range(paginas-1, paginas+1)]
        archivos = [formarArchivo(n, archivos_LaVoz)
                    for n in range(nro, nro+2)]

        scrapMultiHilo(URLs, archivos)

    escribirFechaArchivo()


if __name__ == "__main__":
    main()
