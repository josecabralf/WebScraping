from archivosDF import crearArchivoDF
from PDconfig import *


def crearDataFramesInmuebles():
    """Crea una serie de archivos CSV que contienen un DataFrame cada uno. Estos archivos se corresponden con cada una de las páginas que se ha scrapeado: LaVoz, MercadoLibre, ZonaProp.
    """
    crearArchivoDF(path_LV, df_LV)
    crearArchivoDF(path_ML, df_ML)
    crearArchivoDF(path_ZP, df_ZP)


def main():
    crearDataFramesInmuebles()


if __name__ == "__main__":
    main()
