from config import revisionesFecha


def agregarRevisionArchivo(URL):
    """Agrega una url al archivo de revisiones de fecha para posteriormente poder correr un proceso para recuperar el dato de la publicacion

    Args:
        URL (string): url de la publicacion
    """
    file = open(revisionesFecha, 'a')
    file.write(URL + '\n')
    file.close()
