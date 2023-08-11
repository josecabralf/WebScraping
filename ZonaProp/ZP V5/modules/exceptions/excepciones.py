from ZPConfig import revisionesFecha


def agregarRevisionArchivo(URL, id):
    """Agrega una url al archivo de revisiones de fecha para posteriormente poder correr un proceso para recuperar el dato de la publicacion

    Args:
        URL (string): url de la publicacion
        id (int): id de la publicacion
    """
    file = open(revisionesFecha, 'a')
    file.write(f'{id} {URL}\n')
    file.close()
