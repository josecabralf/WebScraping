import numpy as np


def cambiarValoresNull(df):
    df = df.replace(-1, np.nan)
    return df


def formatearDF(df):
    del df['URL']
    df = cambiarValoresNull(df)
    return df