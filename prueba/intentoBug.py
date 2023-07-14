import json

l = [
    {
        "id": "5081118",
        "tipoPropiedad": "CASA",
        "precioUSD": 65500,
        "fechaUltimaActualizacion": "11-07-2023",
        "terrenoTotal": 243,
        "terrenoEdificado": 88,
        "cantDormitorios": 3,
        "cantBanos": 1,
        "cantCochera": 1,
        "barrio": "PARQUE CAPITAL",
        "ciudad": "C\u00d3RDOBA",
        "URL": "https://clasificados.lavoz.com.ar/avisos/casas/5081118/apto-credito-con-certificado-excelente-zona-a-modernizar-gran-patio"
    }, {
        "id": "4971778",
        "tipoPropiedad": "DEPARTAMENTO",
        "precioUSD": 37000,
        "fechaUltimaActualizacion": "11-07-2023",
        "terrenoTotal": 35,
        "terrenoEdificado": -1,
        "cantDormitorios": 1,
        "cantBanos": 1,
        "cantCochera": -1,
        "barrio": "PUEYRREDON",
        "ciudad": "C\u00d3RDOBA",
        "URL": "https://clasificados.lavoz.com.ar/avisos/departamentos/4971778/venta-departamento-pueyrredon-1-dormitorio-apto-credito"
    }, {
        "id": "5043215",
        "tipoPropiedad": "DEPARTAMENTO",
        "precioUSD": 65000,
        "fechaUltimaActualizacion": "11-07-2023",
        "terrenoTotal": 0,
        "terrenoEdificado": -1,
        "cantDormitorios": 1,
        "cantBanos": 1,
        "cantCochera": -1,
        "barrio": "GENERAL PAZ",
        "ciudad": "C\u00d3RDOBA",
        "URL": "https://clasificados.lavoz.com.ar/avisos/departamentos/5043215/a-estrenar-balcon-dormitorio-muy-amplio"
    }
]
archivo = './ar.json'
with open(archivo, 'w') as archivoJSON:
    json.dump(l, archivoJSON, indent=12)
