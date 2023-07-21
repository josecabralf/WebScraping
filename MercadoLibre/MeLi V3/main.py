from MeLiConfig import archivos_Links, leidos_links, archivos_Meli, publicadosHoy, errores_links
from archivosLinks import crearArchivoLinksSiNoExiste
from scraperMeLi import scrapLinkMeLi
import os


def abrirArchivo(flag):
    """Abre un archivo que posee links de busquedas filtradas. En caso de que dicho archivo no exista, lo crea.

    Args:
        flag (bool): indica si hubo un scrap previo

    Returns:
        txt file: archivo txt que posee links filtrados
    """
    if flag:
        try:
            archivo = open(archivos_Links, 'r')
        except:
            print('Creando Archivo...')
            crearArchivoLinksSiNoExiste()
            archivo = open(archivos_Links, 'r')
    else:
        archivo = open(publicadosHoy, 'r')

    print('Archivo abierto')
    return archivo


def agregarALeidos(linea, bool):
    if bool:
        f = open(leidos_links, 'a')
        f.write(linea)
        f.close()
    else:
        f = open(errores_links, 'a')
        f.write(linea)
        f.close()


def asignarValNro():
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = os.listdir(archivos_Meli)
    if dir == []:
        return 1
    dir = [int(n.split('-')[0]) for n in dir]
    n = max(dir)
    return n


def main():
    archivo = abrirArchivo((os.listdir(archivos_Meli) == []))

    nro = asignarValNro()
    for line in archivo.readlines():
        print(f'Scrapeando Link {nro}')
        try:
            link = line.replace('\n', '')
            scrapLinkMeLi(link, nro)
            nro += 1
            agregarALeidos(line, True)
        except:
            print(f'No se pudo scrapear Link {nro}')
            agregarALeidos(line, False)
    archivo.close()


if __name__ == "__main__":
    main()
