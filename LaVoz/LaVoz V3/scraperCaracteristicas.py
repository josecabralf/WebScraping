def getDatosCaracteristicas(caracteristicas):
    """Busca caracteristicas deseadas de una lista de caracteristicas presentadas

    Args:
        caracteristicas ([[string]]): lista que posee una serie de listas con caracteristicas encontraadas en una publicacion de La Voz

    Returns:
        [dynamic]: lista de valores de las caracteristicas encontradas
    """
    caracteristicas_deseadas = ['FichaInmueble_tipovivienda', 'FichaInmueble_superficie',
                                'FichaInmueble_dormitorios', 'FichaInmueble_bano', 'menu_vehiculos', 'fichaproductos_ciudad']
    valores = ['', -1, -1, -1, -1, -1, '']
    # Inmueble superficie suele aparecer dos veces: tamaño del terreno, tamaño edificado
    cont_inmueble_superficie = 0

    for dato in caracteristicas:  # Por cada dato encontrado
        # Recorremos cada caracteristica que queremos
        for i in range(len(caracteristicas_deseadas)):
            # y chequeamos si el dato se corresponde con ella
            if dato[0] == caracteristicas_deseadas[i]:

                if dato[0] == 'FichaInmueble_tipovivienda':
                    valores[0] = str(dato[1]).upper()
                elif dato[0] == 'FichaInmueble_superficie':
                    cont_inmueble_superficie += 1
                    valores[cont_inmueble_superficie] = int(dato[1])
                elif dato[0] == 'fichaproductos_ciudad':
                    valores[i+1] = (' '.join(dato[1:len(dato)+1])).upper()
                else:
                    for j in range(1, len(dato)):
                        try:
                            valores[i+1] = int(dato[j])
                            break
                        except:
                            continue
                break

    return valores
