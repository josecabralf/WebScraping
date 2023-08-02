import os
from ZPConfig import archivos_ZonaProp, archivos_filtros, publicados_recientes


def formarArchivo(nro, i, ruta):
    """Forma rutas a archivos para almacenar listados de publicaciones

    Args:
        i (int): indica el numero de pagina actual
        ruta: ruta relativa a la carpeta donde se almacenará el archivo

    Returns:
        string: nombre y ruta del archivo
    """
    return ruta + f"{nro}-pagina{i}.json"


def asignarValNro(directorio):
    """Busca el proximo nro de archivo

        Returns:
            int: proximo nro de archivo
    """
    dir = os.listdir(directorio)
    if dir == []:
        return 1
    dir = [int(n.split('-')[0]) for n in dir]
    n = max(dir)
    return n+1


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
