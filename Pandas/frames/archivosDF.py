import os
import pandas as pd
import datetime
from PDconfig import *
from frames.format import formatearDF


def crearDataFramesInmuebles():
    """Crea una serie de archivos CSV que contienen un DataFrame cada uno. Estos archivos se corresponden con cada una de las páginas que se ha scrapeado: LaVoz, MercadoLibre, ZonaProp.
    """
    crearArchivoDF(path_LV, LaVoz)
    crearArchivoDF(path_ML, MeLi)
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


def cargarTablaMain(path, df_main=pd.DataFrame()):
    """Crea un DataFrame a partir de una lista de archivos CSV

    Returns:
        DataFrame: DataFrame creado a partir de archivos CSV
    """
    dir = os.listdir(path)
    for archivo in dir:
        try:
            path = f"{path}{archivo}"
            df_i = abrirDF(path)
            df_main = df_main._append(df_i, ignore_index=True)
        except:
            continue
    return df_main


def crearArchivoDF(path, archivo):
    """Busca una serie de archivos CSV para luego crear un DataFrame a partir de ellos y guardarlo en un archivo CSV

    Args:
        path ([string]): rutas del directorio con archivos CSV
        archivo (string): ruta del archivo en que se guardara el DataFrame
    """
    for p in path:
        if os.listdir(p) != []:
            df = cargarTablaMain(path, df)
    df = formatearDF(df)
    guardarDF(df, archivo)


def updateDataFrames():
    """Actualiza los archivos CSV que contienen los DataFrames de cada página web. 
    Para ello, se crea un DataFrame con los datos de los archivos CSV que guardan las publicaciones de cada página, se evalúan los campos fecha de las diferentes publicaciones, se actualiza el campo activo; y luego se sobrescribe el Dataframe modificado en el CSV original.
    """
    crearDataFramesInmuebles()
    for datos in [LaVoz, MeLi, ZonaP]:
        df = abrirDF(datos)
        df['fechaUltimaActualizacion'] = pd.to_datetime(
            df['fechaUltimaActualizacion'], format='%d-%m-%Y')
        hoy = datetime.date.today()
        for idx, row in df.iterrows():
            diferencia = (hoy - row['fechaUltimaActualizacion'].date()).days
            if diferencia > 45:
                df.at[idx, 'activo'] = False
        df['fechaUltimaActualizacion'] = df['fechaUltimaActualizacion'].dt.strftime(
            '%d-%m-%Y')
        guardarDF(df, datos)
