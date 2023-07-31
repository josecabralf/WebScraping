from unidecode import unidecode


def getDatosCaracteristicas(caracteristicas, URL):
    """Busca caracteristicas deseadas de una lista de caracteristicas presentadas

    Args:
        caracteristicas ([[string]]): lista que posee una serie de listas con caracteristicas encontraadas en una publicacion de los Clasificados de La Voz

    Returns:
        dict: diccionario deseados de valores de las caracteristicas encontradas
    """
    deseados = {'Tipo vivienda': URL.split('/')[4].replace('-',' ').upper(),
                'Superficie total': -1,
                'Superficie cubierta': -1,
                'Dormitorios': -1,
                'Baños': -1,
                'Cocheras': -1,
                'Barrio': '',
                'Ciudad': ''}

    flag_superficie, flag_ubicacion = False, False

    for dato in caracteristicas:
        if dato[0] == 'FichaInmueble_tipovivienda':
            deseados['Tipo vivienda'] = str(dato[1]).upper()
        elif dato[0] == 'FichaInmueble_superficie':
            if not flag_superficie:
                asignarSuperficie(deseados, dato, 'Superficie total')
                flag_superficie = True
            else:
                asignarSuperficie(deseados, dato, 'Superficie cubierta')
        elif dato[0] == 'fichaproductos_ciudad':
            if not flag_ubicacion:
                asignarUbicacion(deseados, dato, 'Ciudad')
                flag_ubicacion = True
            else:
                asignarUbicacion(deseados, dato, 'Barrio')
        elif dato[0] == 'FichaInmueble_dormitorios':
            asignarDatoVariable(deseados, dato, 'Dormitorios')
        elif dato[0] == 'FichaInmueble_bano':
            asignarDatoVariable(deseados, dato, 'Baños')
        elif dato[0] == 'menu_vehiculos':
            asignarDatoVariable(deseados, dato, 'Cocheras')
    return deseados


def asignarSuperficie(diccionario, arreglo, clave):
    """Asigna al diccionario de caracteristicas el valor de una superficie

    Args:
        diccionario (dict): diccionario de caracteristicas
        arreglo ([string]): arreglo de datos sobre caracteristica especifica
        clave (string): clave del dato a asignar en diccionario [Superficie total / Superficie cubierta]
    """
    try:
        diccionario[clave] = int(
            round(float(arreglo[1]), 0))
    except:
        diccionario[clave] = int(
            round(float(arreglo[1].replace(',', '.').split('m')[0])))


def asignarUbicacion(diccionario, arreglo, clave):
    """Asigna al diccionario de caracteristicas el valor de una ubicacion

    Args:
        diccionario (dict): diccionario de caracteristicas
        arreglo ([string]): arreglo de datos sobre caracteristica especifica
        clave (string): clave del dato a asignar en diccionario [Ciudad / Barrio]
    """
    diccionario[clave] = unidecode(
        (' '.join(arreglo[1:len(arreglo)+1])).upper())


def asignarDatoVariable(diccionario, arreglo, clave):
    """Asigna al diccionario de caracteristicas el valor de una caracteristica que se presenta con formato variable

    Args:
        diccionario (dict): diccionario de caracteristicas
        arreglo ([string]): arreglo de datos sobre caracteristica especifica
        clave (string): clave del dato a asignar en diccionario [Dormitorios / Baños / Cocheras]
    """
    for j in range(1, len(arreglo)):
        try:
            diccionario[clave] = int(arreglo[j])
            break
        except:
            continue
