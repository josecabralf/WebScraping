import os
import datetime
import pandas as pd
from LVConfig import archivo_fecha


def formarArchivo(i, ruta):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return ruta + f"{i}-pagina.csv"


def escribirFechaArchivo():
    """Escribe la fecha del día actual en el archivo de fechaUltimoScrap
    """
    fecha = datetime.date.today()
    f = open(archivo_fecha, 'w')
    f.write(str(fecha.strftime("%d-%m-%Y")))
    f.close()


def recuperarFechaArchivo():
    """Recupera la fecha del último scrap para hacer validaciones

    Returns:
        date: fecha del último scrap
    """
    try:
        f = open(archivo_fecha, 'r')
        fecha = f.readline()
        f.close()
    except:
        return None
    return datetime.datetime.strptime(fecha, "%d-%m-%Y")


def asignarValNro(directorio):
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = os.listdir(directorio)
    if dir == []:
        return 1
    dir = [int(n.split('-')[0]) for n in dir]
    return max(dir) + 1


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

