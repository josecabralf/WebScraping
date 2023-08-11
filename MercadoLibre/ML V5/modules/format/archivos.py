import os
import pandas as pd
from MeLiConfig import archivos_Meli, publicadosHoy, errores_links, archivos_Links, leidos_links
from modules.filters.filtros import crearArchivoLinksSiNoExiste


def formarArchivo(i, ruta, nro):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        nro (int): id de la URL scrapeada
        i (int): indica el numero de pagina actual
        ruta (string): ruta relativa a la carpeta donde se almacenará el archivo
        url (string): url de la pagina a scrapear

    Returns:
        string: nombre y ruta del archivo
    """
    return f"{ruta}{nro}-pagina{i}.csv"


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
    return max(dir)+1


def comprimirCantArchivos(directorio):
    """Reduce la cantidad de archivos producto de scrap del directorio pasado como parametro.

    Args:
        directorio: ruta relativa al directorio de scrapeo
    """
    dir = os.listdir(directorio)
    df_main = pd.DataFrame()
    for archivo in dir:
        if archivo.split('-')[1] != 'comprimido.csv':
            path = f"{directorio}/{archivo}"
            df_i = pd.read_csv(path, sep=';')
            df_main = df_main._append(df_i, ignore_index=True)
            os.remove(path)

    path = f"{directorio}/{asignarValNro(directorio)}-comprimido.csv"
    df_main.to_csv(path, index=False, sep=';')
