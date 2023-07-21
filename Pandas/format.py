def cambiarValoresNull(df):
    df = df.replace(-1, None)
    return df


def formatearDF(df):
    del df['URL']
    df = cambiarValoresNull(df)
    return df