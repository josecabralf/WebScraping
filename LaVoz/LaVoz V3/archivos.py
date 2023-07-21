import os
import datetime
from LVConfig import archivo_fecha, archivos_LaVoz


def formarArchivo(i, ruta):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return ruta + f"pagina{i}.json"


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
    f = open(archivo_fecha, 'r')
    fecha = f.readline()
    f.close()
    return datetime.datetime.strptime(fecha, "%d-%m-%Y")


def asignarValNro(directorio):
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = os.listdir(directorio)
    if dir == []:
        return 1
    dir = [int(n.split('.')[0].split('a')[-1])
           for n in dir]
    n = max(dir)
    return n+1
