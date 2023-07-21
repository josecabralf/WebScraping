from MeLiConfig import archivos_Links, leidos_links, archivos_Meli, publicadosHoy
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



def agregarALeidos(linea):
    """Agrega un link al archivo de ya leidos
    """
    f = open(leidos_links, 'a')
    f.write(linea)
    f.close()


def asignarValNro():
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = [int(n.split('-')[0]) for n in os.listdir(archivos_Meli)]
    n = max(dir)
    return n


def main():
    archivo = abrirArchivo((os.listdir(archivos_Meli) == []))

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
