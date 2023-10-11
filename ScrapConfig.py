"""Archivo de configuraciones para realizar el scrapping de datos de propiedades inmobiliarias.
"""
path_driver = './utils/driver/chromedriver.exe'

cols = 'id;tipoPropiedad;precioUSD;fechaUltimaActualizacion;tipoVendedor;terrenoTotal;terrenoEdificado;cantDormitorios;cantBanos;cantCochera;barrio;ciudad;coordX;coordY;activo;URL\n'
linea_null = "0;-;0;1900-01-01;-;-1;-1;-1;-1;-1;-;-;;;False;-\n"

revision = './utils/Scrap/revision.txt'
logs = './utils/Scrap/logs.txt'

# LA VOZ 
archivos_LV = '../Data/Fuentes/LV/ScrapResults/'
utils_fecha_LV = './utils/Scrap/LV/fechaUltimoScrap.txt'
URL_LV = 'https://clasificados.lavoz.com.ar/inmuebles/todo?provincia=cordoba&operacion=venta'

# MERCADO LIBRE
archivos_ML = '../Data/Fuentes/ML/ScrapResults/'
URL_ML = 'https://inmuebles.mercadolibre.com.ar/venta/propiedades-individuales/cordoba/inmuebles_PublishedToday_YES_NoIndex_True'

# ZONAPROP
archivos_ZP = '../Data/Fuentes/ZP/ScrapResults/'
publicados_reciente_ZP = './utils/Scrap/ZP/reciente.txt'
URL_Base_ZP = 'https://www.zonaprop.com.ar'
URL_ZP = 'https://www.zonaprop.com.ar/casas-departamentos-ph-terrenos-venta-cordoba-publicado-hace-menos-de-15-dias.html'