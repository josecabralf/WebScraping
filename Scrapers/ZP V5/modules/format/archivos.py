import os
import pandas as pd
from ZPConfig import archivos_ZonaProp, archivos_filtros, publicados_recientes, comprimidos


def formarArchivo(i, ruta, nro):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return f"{ruta}{nro}-pagina{i}.csv"


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


def abrirArchivo():
    """Abre un archivo que posee links de busquedas filtradas. En caso de que dicho archivo no exista, lo crea.

    Returns:
        txt file: archivo txt que posee links filtrados
    """
    if os.listdir(archivos_ZonaProp) == []:
        archivo = open(archivos_filtros, 'r')
    else:
        archivo = open(publicados_recientes, 'r')
    return archivo


def comprimirCantArchivos(directorio):
    """Reduce la cantidad de archivos producto de scrap del directorio pasado como parametro.

    Args:
        directorio: ruta relativa al directorio de scrapeo
    """
    dir = os.listdir(directorio)
    df_main = pd.DataFrame()
    for archivo in dir:
        path = f"{directorio}/{archivo}"
        df_i = pd.read_csv(path, sep=';')
        df_main = df_main._append(df_i, ignore_index=True)
        os.remove(path)
        if df_main.shape[0] > 10000000:
            guardarArchivoComprimido(df_main)
            df_main = pd.DataFrame()

    guardarArchivoComprimido(df_main, directorio)


def guardarArchivoComprimido(df, directorio=comprimidos):
    """Guarda un dataframe en un archivo csv

    Args:
        df (DataFrame): datos a guardar
        directorio (str): ruta del directorio en que se desea guardar el archivo
    """
    path = f"{directorio}/{asignarValNro(directorio)}-comprimido.csv"
    df.to_csv(path, index=False, sep=';')
