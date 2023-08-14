import pandas as pd


def filtrarDatosGralML(df):
    """Realiza un filtrado general de los datos de Mercado Libre.

    Args:
        df (DataFrame): DataFrame con los datos de Mercado Libre.

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
    filt = (df["tipoPropiedad"] == "CASA") | (df["tipoPropiedad"]
                                              == "DEPARTAMENTO") | (df["tipoPropiedad"] == "TERRENO")
    df = df.loc[filt]

    # ELIMINAR DATOS SIN CAMPOS RELEVANTES
    filtro_T = (df['terrenoEdificado'] == 1)
    filtro_P = ((df['precioUSD'] == 1))
    df.drop(df[filtro_T | filtro_P].index, inplace=True)
    df.drop(df[df['ciudad'] == 'CAPITAL FEDERAL'].index, inplace=True)

    # ELIMINAR DATOS SIN VALOR VERDADERO
    import numpy as np
    filt = df['barrio'].str.contains('INMUEBLES', na=False)
    df.loc[filt, 'barrio'] = np.nan

    departamentos = ['CALAMUCHITA', 'COLON', 'CRUZ DEL EJE',
                     'GENERAL ROCA', 'GENERAL SAN MARTIN', 'ISCHILIN', 'JUAREZ CELMAN',
                     'MARCOS JUAREZ', 'MINAS', 'POCHO', 'PUNILLA', 'RIO CUARTO', 'RIO PRIMERO',
                     'RIO SECO', 'RIO SEGUNDO', 'SAN ALBERTO', 'SAN JAVIER', 'SAN JUSTO',
                     'SANTA MARIA', 'TERCERO ARRIBA', 'TOTORAL', 'TULUMBA', 'UNION']
    filt = df['ciudad'].isin(departamentos)
    df.loc[filt, 'ciudad'] = df.loc[filt, 'barrio']
    filt = (df['ciudad'] == df['barrio'])
    df.loc[filt, 'barrio'] = np.nan

    return df


def separarYFiltrarTiposPropML(df):
    """Realiza una separación de los datos de Mercado Libre según el tipo de propiedad; y luego realiza un filtrado de los mismos.

    Args:
        df (DataFrame): Datos de Mercado Libre.

    Returns:
        Dataframe, DataFrame, DataFrame: datos de casas filtrados, datos de departamentos filtrados, datos de terrenos filtrados.
    """
    terrenos = df.loc[df["tipoPropiedad"] == "TERRENO"]
    casas = df.loc[df["tipoPropiedad"] == "CASA"]
    deptos = df.loc[df["tipoPropiedad"] == "DEPARTAMENTO"]

    # FILTRADO DEPARTAMENTOS
    filt1 = (deptos['terrenoEdificado'] < 15) | (
        deptos['terrenoEdificado'].isna())
    filt2 = deptos['terrenoTotal'].notna()
    deptos.loc[filt1 & filt2,
               'terrenoEdificado'] = deptos.loc[filt1 & filt2, 'terrenoTotal']

    filtro_P = deptos["precioUSD"].between(deptos["precioUSD"].quantile(0.005),
                                           deptos["precioUSD"].quantile(0.995))
    filtro_E = (deptos["terrenoEdificado"].between(10, 1500))
    deptos = deptos.loc[filtro_P & filtro_E]

    # FILTRADO CASAS
    filtro_P = casas["precioUSD"].between(casas["precioUSD"].quantile(0.005),
                                          casas["precioUSD"].quantile(0.995))
    filtro_E = casas['terrenoEdificado'].between(15, 2500)
    filtro_T = (casas['terrenoTotal'].between(casas['terrenoTotal'].quantile(0.001),
                                              casas['terrenoTotal'].quantile(0.95))) | casas['terrenoTotal'].isna()
    casas = casas.loc[filtro_P & filtro_E & filtro_T]

    # FILTRADO TERRENOS
    filtro_P = terrenos["precioUSD"].between(1500, 1000000)
    filtro_T = (terrenos['terrenoTotal'].between(terrenos['terrenoTotal'].quantile(0.005),
                                                 terrenos['terrenoTotal'].quantile(0.995)))
    terrenos = terrenos.loc[filtro_P & filtro_T]

    return casas, deptos, terrenos
