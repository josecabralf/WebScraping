import pandas as pd
from frames.analisis.plotter import plotGraficoBarrasInmueble


def analizarInmueble(df_tipo, archivoExcel, img, nombreTipo):
    """Realiza un analisis del precio por m2 de un tipo de propiedad en la ciudad de Cordoba.

    Args:
        df_tipo (DataFrame): datos del tipo de propiedad
        archivoExcel (str): ruta al archivo excel donde se guardaran los resultados
        img (str): ruta al archivo de imagen donde se guardara el grafico
        nombreTipo (str): tipo de propiedad
    """
    df_tipo['$/m2_total'] = df_tipo['precioUSD'] / df_tipo['terrenoTotal']
    df_tipo['$/m2_edif'] = df_tipo['precioUSD'] / df_tipo['terrenoEdificado']

    tipo_filtro = df_tipo.loc[df_tipo['ciudad'] == 'CORDOBA']
    barrios = tipo_filtro.groupby(['ciudad', 'barrio'])

    precio_m2_total_prom = barrios['$/m2_total'].mean().round(0)
    precio_m2_total_med = barrios['$/m2_total'].median().round(0)
    precio_m2_edif_prom = barrios['$/m2_edif'].mean().round(0)
    precio_m2_edif_med = barrios['$/m2_edif'].median().round(0)
    cantidad = barrios.size()

    resultados = pd.DataFrame({
        'Precio_m2_total_promedio': precio_m2_total_prom,
        'Precio_m2_total_mediana': precio_m2_total_med,
        'Precio_m2_edif_promedio': precio_m2_edif_prom,
        'Precio_m2_edif_mediana': precio_m2_edif_med,
        'Cantidad': cantidad
    })
    resultados.reset_index(inplace=True)
    results_df = resultados[['ciudad', 'barrio', 'Precio_m2_edif_promedio', 'Precio_m2_edif_mediana',
                             'Precio_m2_total_promedio', 'Precio_m2_total_mediana', 'Cantidad']]

    results_df.to_excel(archivoExcel, index=False)
    plotGraficoBarrasInmueble(resultados, img, nombreTipo)
