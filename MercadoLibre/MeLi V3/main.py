from MeLiConfig import archivos_Links, leidos_links, archivos_Meli
from archivosLinks import crearArchivoLinksSiNoExiste
from scraperMeLi import scrapLinkMeLi
import os


def abrirArchivo():
    """Abre un archivo que posee links de busquedas filtradas. En caso de que dicho archivo no exista, lo crea.

    Returns:
        txt file: archivo txt que posee links filtrados
    """
    try:
        archivo_post_filtro = open(archivos_Links, 'r')
    except:
        print('Creando Archivo...')
        crearArchivoLinksSiNoExiste()
        archivo_post_filtro = open(archivos_Links, 'r')

    print('Archivo abierto')
    return archivo_post_filtro


def agregarALeidos(linea):
    f = open(leidos_links, 'a')
    f.write(linea)
    f.close()


def asignarValNro():
    dir = [int(n.split('-')[0]) for n in os.listdir(archivos_Meli)]
    n = max(dir)
    return n


def main():
    archivo = abrirArchivo()
    nro = asignarValNro()
    for line in archivo.readlines():
        print(f'Scrapeando Link {nro}')
        link = line.replace('\n', '')
        scrapLinkMeLi(link, nro)
        nro += 1
        agregarALeidos(line)
    archivo.close()


if __name__ == "__main__":
    main()
