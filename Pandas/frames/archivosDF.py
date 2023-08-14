import os
import pandas as pd
from PDconfig import *
from frames.format import formatearDF


def crearDataFramesInmuebles():
    """Crea una serie de archivos CSV que contienen un DataFrame cada uno. Estos archivos se corresponden con cada una de las páginas que se ha scrapeado: LaVoz, MercadoLibre, ZonaProp.
    """
    if not os.path.exists(LaVoz):
        crearArchivoDF(path_LV, LaVoz)
    if not os.path.exists(MeLi):
        crearArchivoDF(path_ML, MeLi)
    if not os.path.exists(ZonaP):
        crearArchivoDF(path_ZP, ZonaP)


def abrirDF(path, col=False):
    """Abre un archivo CSV extrayendo los datos de la df que contiene

    Args:
        path (string): localizacion del archivo csv
        cols (string): columna que se quiere que sea indice

    Returns:
        DataFrame: df contenida en el archivo
    """
    if not col:
        return pd.read_csv(path, sep=';')
    return pd.read_csv(path, sep=';', index_col=col)


def guardarDF(df, archivo):
    """Guarda una df en un archivo CSV

    Args:
        df (DataFrame): df con datos a guardar
        archivu: localizacion del archivo csv que se quiere crear
    """
    df.to_csv(archivo, index=False, sep=';')


def cargarTablaMain(path):
    """Crea un DataFrame a partir de una lista de archivos CSV

    Returns:
        DataFrame: DataFrame creado a partir de archivos CSV
    """
    dir = os.listdir(path)
    df_main = pd.DataFrame()
    for archivo in dir:
        try:
            path = f"{path}{archivo}"
            df_i = abrirDF(path)
            df_main = df_main._append(df_i, ignore_index=True)
        except:
            print(archivo)
    return df_main


def crearArchivoDF(path, archivo):
    """Busca una serie de archivos CSV para luego crear un DataFrame a partir de ellos y guardarlo en un archivo CSV

    Args:
        path (string): ruta del directorio con archivos CSV
        archivo (string): ruta del archivo en que se guardara el DataFrame
    """
    df = cargarTablaMain(path)
    df = formatearDF(df)
    guardarDF(df, archivo)
