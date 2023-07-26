import numpy as np


def cambiarValoresNull(df):
    df = df.replace(-1, np.nan)
    return df


def eliminarDuplicados(df):
    df = df.drop_duplicates(subset='id', keep='last',
                            ignore_index=False)
    return df


def eliminarNulos(df):
    df = df.dropna(how="all", subset=[
                   'terrenoTotal', 'terrenoEdificado', 'cantDormitorios', 'cantBanos', 'cantCochera'])
    return df


def formatearDF(df):
    del df['URL']
    df = cambiarValoresNull(df)
    df = eliminarDuplicados(df)
    df = eliminarNulos(df)
    return df
