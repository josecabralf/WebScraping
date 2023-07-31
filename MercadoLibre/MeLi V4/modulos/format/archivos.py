import datetime
import os
from MeLiConfig import archivos_Meli, publicadosHoy, errores_links, archivos_Links, leidos_links
from modules.filters.filtros import crearArchivoLinksSiNoExiste


def formarArchivo(nro, i, ruta, URL):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        nro (int): id de la URL scrapeada
        i (int): indica el numero de pagina actual
        ruta (string): ruta relativa a la carpeta donde se almacenará el archivo
        url (string): url de la pagina a scrapear

    Returns:
        string: nombre y ruta del archivo
    """
    nom_base = URL.split('/')
    try:
        ar = '-'.join([f'{nro}', nom_base[6], nom_base[7], f'{i+1}.json'])
    except:
        ar = '-'.join([f'{nro}',
                      datetime.date.today().strftime("%d_%m_%Y"), f'{i+1}.json'])
    return ruta + ar


def abrirArchivo():
    """Abre un archivo que posee links de busquedas filtradas. En caso de que dicho archivo no exista, lo crea.

    Returns:
        txt file: archivo txt que posee links filtrados
    """
    if os.listdir(archivos_Meli) == []:
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


def asignarValNro(directorio):
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = os.listdir(directorio)
    if dir == []:
        return 1
    dir = [int(n.split('-')[0]) for n in dir]
    n = max(dir)
    return n+1
