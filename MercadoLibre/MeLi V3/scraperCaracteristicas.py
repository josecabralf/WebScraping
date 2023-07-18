def getDatosCaracteristicas(caracteristicas):
    """Recibe un objeto BeautifulSoup que representa una etiqueta tbody de HTML y busca las caracteristicas deseadas de la misma

    Args:
        caracteristicas (BeautifulSoup): tbody HTML que contiene caracteristicas deseadas

    Returns:
        dict: diccionario con las caracteristicas deseadas
    """
    headers = caracteristicas.find_all('th')
    body = caracteristicas.find_all('td')

    deseados = {'Superficie total': -1,
                'Superficie cubierta': -1,
                'Dormitorios': -1,
                'Baños': -1,
                'Cocheras': -1}

    for i in range(len(headers)):
        car = headers[i].text
        if car in deseados:
            val = body[i].text.split()[0]
            try:
                deseados[car] = int(val)
            except:
                deseados[car] = int(round(float(val), 0))

    return deseados
