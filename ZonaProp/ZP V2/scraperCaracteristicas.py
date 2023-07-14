def getDatosCaracteristicas(caracteristicas):
    """Recibe una lista de caracteristicas obtenidas de HTML y busca las caracteristicas deseadas de la misma

    Args:
        caracteristicas ([string]): lista de caracteristicas

    Returns:
        dict: diccionario con las caracteristicas deseadas
    """

    deseados = {'m² Total': -1,
                'm² Cubierta': -1,
                'Dormitorios': -1,
                'Baños': -1,
                'Cocheras': -1}

    for car in caracteristicas:
        car = car.split('\n')
        try:
            if car[1] in deseados:
                deseados[car[1]] = car[0]
            elif car[1][-1] != 's':
                car[1] = car[1] + 's'
                if car[1] in deseados:
                    deseados[car[1]] = car[0]
        except: continue
    return deseados