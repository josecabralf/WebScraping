from MeLiConfig import archivos_Links
from archivosLinks import crearArchivoLinksSiNoExiste
from scraperMeLi import scrapLinkMeLi


def abrirArchivo():
    """Abre un archivo que posee links de busquedas filtradas. En caso de que dicho archivo no exista, lo crea.

    Returns:
        file: archivo txt que posee links filtrados
    """
    try:
        archivo_post_filtro = open(archivos_Links, 'r')
    except:
        print('Creando Archivo...')
        crearArchivoLinksSiNoExiste()
        archivo_post_filtro = open(archivos_Links, 'r')

    return archivo_post_filtro


def main():
    archivo = abrirArchivo()
    for line in archivo.readlines():
        link = line.replace('\n', '')
        scrapLinkMeLi(link)

    archivo.close()


if __name__ == "__main__":
    main()
