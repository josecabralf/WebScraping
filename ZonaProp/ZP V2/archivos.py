import os


def formarArchivo(i, ruta):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return ruta + f"pagina{i}.json"


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
