from soup import getSoup


def getCaracteristicasTerreno(URL):
    """Busca una etiqueta span dentro de la pagina de una publicacion de inmuebles de Mercado Libre que contiene el terreno total.
    La razón por la que posee un while es porque Mercado Libre no siempre renderiza la publicacion de la misma manera, por lo que hay veces en que la tabla no existe. En esos casos se repite el proceso hasta que se la obtiene.

    Args:
        URL (string): url de la publicacion del inmueble

    Returns:
        dict: diccionario con datos de interes
    """
    i = 0
    while True:
        i += 1
        soup = getSoup(URL)
        terreno = soup.find(
            "span", class_="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label")
        if terreno:
            terreno = terreno.text
            break
        if i == 8:
            return False
    terreno = int(round(float(terreno.split()[0]), 0))
    datos_interes = {'Superficie total': terreno,
                     'Superficie cubierta': -1,
                     'Dormitorios': -1,
                     'Baños': -1,
                     'Cocheras': -1}
    return datos_interes


def getCaracteristicasInmueble(URL):
    """Busca una etiqueta tbody dentro de la pagina de una publicacion de inmuebles de Mercado Libre.
    La razón por la que posee un while es porque Mercado Libre no siempre renderiza la publicacion de la misma manera, por lo que hay veces en que la tabla no existe. En esos casos se repite el proceso hasta que se la obtiene.

    Args:
        URL (string): url de la publicacion del inmueble

    Returns:
        dict: diccionario con datos de interes
    """
    i = 0
    while True:
        i += 1
        soup = getSoup(URL)
        caracteristicas = soup.find("tbody", class_="andes-table__body")
        if caracteristicas:
            break
        if i == 8:
            return False

    datos_interes = getDatosCaracteristicas(caracteristicas)
    return datos_interes


def getCaracteristicas(URL, tipo_prop):
    """Busca las caracteristicas de interes de una propiedad dependiendo de su tipo.

    Args:
        URL (string): url de la publicacion del inmueble
        tipo_prop (string): tipo de propiedad

    Returns:
        dict: diccionario con datos de interes
    """
    if tipo_prop == "TERRENO":
        return getCaracteristicasTerreno(URL)

    return getCaracteristicasInmueble(URL)


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
