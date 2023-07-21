from archivosDF import crearArchivoDF
from PDconfig import *
import pandas as pd
import os


def crearDataFramesInmuebles():
    """Crea una serie de archivos CSV que contienen un DataFrame cada uno. Estos archivos se corresponden con cada una de las páginas que se ha scrapeado: LaVoz, MercadoLibre, ZonaProp.
    """
    if not os.path.exists(df_LV):
        crearArchivoDF(path_LV, df_LV)
    #crearArchivoDF(path_ML, df_ML)
    #crearArchivoDF(path_ZP, df_ZP)


def abrirDF(path):
    return pd.read_csv(path, sep=';')


def main():
    crearDataFramesInmuebles()

if __name__ == "__main__":
    main()
