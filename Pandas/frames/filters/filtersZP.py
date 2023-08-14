import pandas as pd


def filtrarDatosGralZP(df):
    """Realiza un filtrado general de los datos de ZonaProp.

    Args:
        df (DataFrame): DataFrame con los datos de ZonaProp.

    Returns:
        DataFrame: DataFrame filtrado.
    """
    df.drop_duplicates(subset='id', keep='last',
                       inplace=True, ignore_index=False)
    df.dropna(how="all", subset=['terrenoTotal',
              'terrenoEdificado'], inplace=True)

    df['fechaUltimaActualizacion'] = pd.to_datetime(
        df['fechaUltimaActualizacion'], format='%d-%m-%Y')
    df['fechaUltimaActualizacion'] = df['fechaUltimaActualizacion'].dt.strftime(
        '%d-%m-%Y')

    df.sort_values(by='fechaUltimaActualizacion',
                   ascending=False, inplace=True)
    df.drop_duplicates(
        subset=['coordX', 'coordY', 'precioUSD'], inplace=True, ignore_index=True)

    # ELIMINAR TIPO PROP INSERVIBLES
    filt = df['tipoPropiedad'] == 'PH'
    df.loc[filt, 'tipoPropiedad'] = "DEPARTAMENTO"

    # ELIMINAR DATOS SIN CAMPOS RELEVANTES
    filtro_T = (df['terrenoEdificado'] == 1)
    filtro_P = ((df['precioUSD'] == 1))
    df.drop(df[filtro_T | filtro_P].index, inplace=True)

    return df


def separarYFiltrarTiposPropZP(df):
    """Realiza una separación de los datos de Mercado Libre según el tipo de propiedad; y luego realiza un filtrado de los mismos.

    Args:
        df (DataFrame): Datos de Mercado Libre.

    Returns:
        Dataframe, DataFrame, DataFrame: datos de casas filtrados, datos de departamentos filtrados, datos de terrenos filtrados.
    """
    # FILTRADO DEPARTAMENTOS
    deptos = df.loc[df["tipoPropiedad"] == "DEPARTAMENTO"]
    filt1 = (deptos['terrenoEdificado'] < 15) | (
        deptos['terrenoEdificado'].isna())
    filt2 = deptos['terrenoTotal'].notna()
    deptos.loc[filt1 & filt2,
               'terrenoEdificado'] = deptos.loc[filt1 & filt2, 'terrenoTotal']

    filtro_P = deptos["precioUSD"].between(deptos["precioUSD"].quantile(0.005),
                                           deptos["precioUSD"].quantile(0.995))
    filtro_E = (deptos["terrenoEdificado"].between(15, 500))
    deptos = deptos.loc[filtro_P & filtro_E]

    # FILTRADO CASAS
    casas = df.loc[df["tipoPropiedad"] == "CASA"]
    filt1 = (casas['terrenoTotal'] < casas['terrenoEdificado'])
    total = casas.loc[filt1, 'terrenoTotal']
    edif = casas.loc[filt1, 'terrenoEdificado']
    casas.loc[filt1, 'terrenoTotal'] = edif
    casas.loc[filt1, 'terrenoEdificado'] = total

    filtro_P = casas["precioUSD"].between(casas["precioUSD"].quantile(0.005),
                                          casas["precioUSD"].quantile(0.995))
    filtro_E = casas['terrenoEdificado'].between(25, 2000)
    filtro_T = (casas['terrenoTotal'].between(casas['terrenoTotal'].quantile(0.001),
                                              casas['terrenoTotal'].quantile(0.999))) | casas['terrenoTotal'].isna()
    casas = casas.loc[filtro_P & filtro_E & filtro_T]

    # FILTRADO TERRENOS
    terrenos = df.loc[df["tipoPropiedad"] == "TERRENOS"]
    filtro_P = terrenos["precioUSD"].between(
        1500, terrenos["precioUSD"].quantile(0.995))
    filtro_T = (terrenos['terrenoTotal'].between(terrenos['terrenoTotal'].quantile(0.005),
                                                 terrenos['terrenoTotal'].quantile(0.995)))
    terrenos = terrenos.loc[filtro_P & filtro_T]

    return casas, deptos, terrenos
