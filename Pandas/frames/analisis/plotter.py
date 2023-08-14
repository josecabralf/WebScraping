import matplotlib.pyplot as plt


def plotGraficoBarrasInmueble(resultados, img, nombreTipo):
    """Genera un grafico de Barras sobre los resultados de un tipo de propiedad

    Args:
        resultados (DataFrame): resultados de un tipo de propiedad
        img (str): ruta de la imagen a guardar
        nombreTipo (str): tipo de propiedad
    """
    resultados.sort_values("Precio_m2_edif_promedio",
                           ascending=False, inplace=True)
    resultados = resultados[(resultados["Cantidad"] > 20)]

    plt.figure(figsize=(12, 6))
    nombresBarrios = resultados['barrio']
    anchoBarra = 0.5

    plt.bar(nombresBarrios, resultados['Precio_m2_edif_promedio'],
            width=anchoBarra, label='Promedio $/m2 Edificado', color='blue')

    plt.bar(nombresBarrios, resultados['Precio_m2_edif_mediana'],
            width=anchoBarra, label='Mediana $/m2 Edificado', color='orange', align='edge')

    plt.xticks(rotation=90)
    plt.xlabel('Barrio')
    plt.ylabel('$/m2')
    plt.title(f'$/m2 Edificado de {nombreTipo} en cada Barrio')
    plt.legend()
    plt.tight_layout()

    plt.savefig(img)
