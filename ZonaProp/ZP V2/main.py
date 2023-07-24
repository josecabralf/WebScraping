from ZPConfig import archivos_ZonaProp, URL_ZonaProp as url
from soup import getSoup
from math import trunc
from hilos import *
from archivos import formarArchivo, asignarValNro
from links import formarLink


def main():
    print("Inicio...")
    soup = getSoup(url)
    publicaciones = int(soup.find('h1').text.split()[0].replace('.', ''))
    paginas = int(trunc(publicaciones / 20))
    print(f"Hay {paginas} a scrapear.")
    del soup
    del publicaciones
    nro = asignarValNro(archivos_ZonaProp)
    for i in range(1, paginas-1, 3):
        links = [formarLink(n, url) for n in range(i, i+3)]
        archivos = [formarArchivo(n, archivos_ZonaProp)
                    for n in range(nro, nro+3)]
        nro += 3
        scrapMultiHilo(links, archivos)

    if paginas % 3 == 1:
        scrapHilo(formarLink(paginas, url),
                  formarArchivo(paginas, archivos_ZonaProp))

    if paginas % 3 == 2:
        links = [formarLink(n, url) for n in range(paginas-1, paginas+1)]
        archivos = [formarArchivo(n, archivos_ZonaProp)
                    for n in range(nro, nro+2)]

        scrapMultiHilo(links, archivos)


if __name__ == "__main__":
    main()
