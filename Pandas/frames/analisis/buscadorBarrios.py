def buscarPublicacionesBarrio(df, archivoExcel, barrio, ciudad='CORDOBA'):
    """Busca las publicaciones de un barrio en particular y las guarda en un archivo Excel

    Args:
        df (DataFrame): datos de todas las publicaciones
        archivoExcel (str): ruta del archivo Excel donde se guardaran los resultados
        barrio (str): barrio a buscar
        ciudad (str, optional): ciudad del barrio. Defaults to 'CORDOBA'.
    """

    filt = (df['barrio'].str.contains(barrio) | df['URL'].str.contains(
        barrio)) & (df['ciudad'] == ciudad) & df['activo']
    resultados = df[filt]
    results_df = resultados[['id', 'tipoPropiedad', 'precioUSD', 'fechaUltimaActualizacion', 'vendedor',
                             'terrenoTotal', 'terrenoEdificado', 'cantDormitorios', 'cantBanos', 'cantCochera', 'barrio', 'URL']]
    results_df.to_excel(archivoExcel, index=False)
    return resultados
