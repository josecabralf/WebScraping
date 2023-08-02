from modules.scrapers.scraperZonaProp import scrapPaginaZonaProp
from ZPConfig import archivos_ZonaProp
from modules.format.archivos import abrirArchivo, asignarValNro


def main():
    archivo = abrirArchivo()
    nro = asignarValNro(archivos_ZonaProp)
    for line in archivo.readlines():
        link = line.replace('\n', '')
        print(f'Scrapeando Link {nro}: {link}')
        scrapPaginaZonaProp(link, nro)
        nro += 1
    archivo.close()


if __name__ == "__main__":
    main()
