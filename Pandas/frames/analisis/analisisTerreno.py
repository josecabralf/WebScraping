from frames.analisis.mapping import mappingCapitalTerrenosGrandes


def buscarTerrenosAptoDuplex(terrenos, archivoExcel):
    filt = (terrenos['URL'].str.contains('apto') |
            terrenos['URL'].str.contains('dup')) & terrenos['activo']
    resultados = terrenos.loc[filt]
    results_df = resultados[['id', 'precioUSD',
                             'terrenoTotal', 'fechaUltimaActualizacion', 'URL']]
    results_df.to_excel(archivoExcel, index=False)
    return results_df


def buscarTerrenosGrandes(terrenos, archivoExcel, img):
    filt = (terrenos['terrenoTotal'] >= 10000) & (
        terrenos['ciudad'] == 'CORDOBA') & terrenos['activo']
    terrenos_grandes = terrenos.loc[filt]

    filt = (terrenos_grandes['coordY'].between(-64.3125, -64.0475)
            & terrenos_grandes['coordX'].between(-31.5325, -31.2975))
    resultados = terrenos_grandes.loc[filt]

    results_df = resultados[['id', 'precioUSD', 'terrenoTotal', 'URL']]
    results_df.to_excel(archivoExcel, index=False)
    mappingCapitalTerrenosGrandes(resultados, img)
