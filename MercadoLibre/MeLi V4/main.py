from modules.scrapers.scraperMeLi import scrapPaginaMeLi
from MeLiConfig import archivos_Meli
from modules.format.archivos import *


def main():
    archivo = abrirArchivo()
    nro = asignarValNro(archivos_Meli)
    for line in archivo.readlines():
        try:
            link = line.replace('\n', '')
            print(f'Scrapeando Link {nro}: {link}')
            scrapPaginaMeLi(link, nro)
            nro += 1
            agregarALeidos(line, True)
        except:
            print(f'No se pudo scrapear Link {nro}')
            agregarALeidos(line, False)
    archivo.close()


if __name__ == "__main__":
    main()
