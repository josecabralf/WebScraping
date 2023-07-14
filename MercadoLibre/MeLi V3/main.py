from MeLiConfig import archivos_Links
from archivosLinks import crearArchivoLinksSiNoExiste
from scraperMeLi import scrapLinkMeLi


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


def main():
    archivo = abrirArchivo()
    for nro, line in enumerate(archivo.readlines()):
        print(f'Scrapeando Link {nro}')
        link = line.replace('\n', '')
        scrapLinkMeLi(link, nro)
    archivo.close()


if __name__ == "__main__":
    main()
