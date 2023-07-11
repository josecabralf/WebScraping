def getDatosCaracteristicas(caracteristicas):
    """Recibe un objeto BeautifulSoup que representa una etiqueta tbody de HTML y busca las caracteristicas deseadas de la misma

    Args:
        caracteristicas (BeautifulSoup): tbody HTML que contiene caracteristicas deseadas

    Returns:
        dict: diccionario con las caracteristicas deseadas
    """
    headers = [th.text for th in caracteristicas.find_all('th')]
    body = [td.text for td in caracteristicas.find_all('td')]

    deseados = {'Superficie total': -1,
                'Superficie cubierta': -1,
                'Dormitorios': -1,
                'Baños': -1,
                'Cocheras': -1}

    for i in range(len(headers)):
        if headers[i] in deseados:
            try:
                deseados[headers[i]] = int(body[i].split()[0])
            except:
                deseados[headers[i]] = int(round(float(body[i].split()[0]), 0))

    return deseados
