def getDatosCaracteristicas(caracteristicas):
    """Busca caracteristicas deseadas de una lista de caracteristicas presentadas

    Args:
        caracteristicas ([[string]]): lista que posee una serie de listas con caracteristicas encontraadas en una publicacion de La Voz

    Returns:
        dict: diccionario de valores de las caracteristicas encontradas
    """


def getDatosCaracteristicas(caracteristicas):

    deseados = {'Tipo vivienda': '',
                'Superficie total': -1,
                'Superficie cubierta': -1,
                'Dormitorios': -1,
                'Baños': -1,
                'Cocheras': -1,
                'Barrio': '',
                'Ciudad': ''}

    cont_inmueble_superficie, cont_fichaproductos_ciudad = 0, 0

    for dato in caracteristicas:
        if dato[0] == 'FichaInmueble_tipovivienda':
            deseados['Tipo vivienda'] = str(dato[1]).upper()
        elif dato[0] == 'FichaInmueble_superficie':
            if cont_inmueble_superficie == 0:
                deseados['Superficie total'] = int(dato[1])
                cont_inmueble_superficie += 1
            else:
                deseados['Superficie cubierta'] = int(dato[1])
        elif dato[0] == 'fichaproductos_ciudad':
            if cont_fichaproductos_ciudad == 0:
                deseados['Ciudad'] = (
                    ' '.join(dato[1:len(dato)+1])).upper()
                cont_fichaproductos_ciudad += 1
            else:
                deseados['Barrio'] = (
                    ' '.join(dato[1:len(dato)+1])).upper()
        elif dato[0] == 'FichaInmueble_dormitorios':
            for j in range(1, len(dato)):
                try:
                    deseados['Dormitorios'] = int(dato[j])
                    break
                except:
                    continue
        elif dato[0] == 'FichaInmueble_bano':
            for j in range(1, len(dato)):
                try:
                    deseados['Baños'] = int(dato[j])
                    break
                except:
                    continue
        elif dato[0] == 'menu_vehiculos':
            for j in range(1, len(dato)):
                try:
                    deseados['Cocheras'] = int(dato[j])
                    break
                except:
                    continue

    return deseados
