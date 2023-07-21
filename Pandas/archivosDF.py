import json
import os
import pandas as pd
from format import formatearDF
from PDconfig import utils_dir


def buscarArchivosJSON(path):
    """Busca todos los archivos JSON de un directorio y escribe sus rutas en un archivo direcciones.txt

    Args:
        path (string): ruta del directorio con archivos JSON
    """
    dir = os.listdir(path)
    direcciones = open(utils_dir, 'a')
    for file in dir:
        if '.json' in file:
            direcciones.write(path + file + '*\n')
    direcciones.close()


def cargarTablaMain():
    """Crea un DataFrame a partir de una lista de archivos JSON

    Returns:
        DataFrame: DataFrame creado a partir de archivos JSON
    """
    direcciones = open(utils_dir, 'r')
    df_main = pd.DataFrame()
    for line in direcciones:
        line = line.split('*')[0]
        archivo = open(line, 'r')
        df_i = pd.DataFrame(json.load(archivo))
        archivo.close()
        df_main = df_main._append(df_i, ignore_index=True)
    return df_main


def crearArchivoDF(path, archivo):
    """Busca una serie de archivos JSON para luego crear un DataFrame a partir de ellos y guardarlo en un archivo CSV

    Args:
        path (string): ruta del directorio con archivos JSON
        archivo (string): ruta del archivo en que se guardara el DataFrame
    """
    if os.path.isfile(utils_dir):
        os.remove(utils_dir)
    buscarArchivosJSON(path)
    df = cargarTablaMain()
    df = formatearDF(df)
    df.to_csv(archivo, index=False, sep=';')
