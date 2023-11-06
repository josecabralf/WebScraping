# ======================================================================================================================
# ======================================================================================================================
# LOGS

logs_scrap = './utils/logs/errors.txt'
logs_operaciones = './utils/logs/operations.txt'
logs_uploads = './utils/logs/uploads.txt'

# ======================================================================================================================
# ======================================================================================================================
# SCRAP CONFIGS

path_driver = './utils/driver/chromedriver.exe'

revision = './utils/Scrap/revision.txt'
fechas = './utils/Scrap/ultimoScrap.csv'

cols = 'id;tipoPropiedad;precioUSD;fechaUltimaActualizacion;vendedor;terrenoTotal;terrenoEdificado;cantDormitorios;cantBanos;cantCochera;barrio;ciudad;coordX;coordY;URL\n'
linea_null = "0;-;0;1900-01-01;-;-1;-1;-1;-1;-1;-;-;;;-\n"

scrap_results_LV = '../Data/Fuentes/LV/ScrapResults/'
URL_LV = 'https://clasificados.lavoz.com.ar/inmuebles/todo?provincia=cordoba&operacion=venta'

scrap_results_ML = '../Data/Fuentes/ML/ScrapResults/'
URL_ML = 'https://inmuebles.mercadolibre.com.ar/venta/propiedades-individuales/cordoba/inmuebles_PublishedToday_YES_NoIndex_True'

scrap_results_ZP = '../Data/Fuentes/ZP/ScrapResults/'
URL_Base_ZP = 'https://www.zonaprop.com.ar'
URL_ZP = 'https://www.zonaprop.com.ar/casas-departamentos-ph-terrenos-venta-cordoba-publicado-hace-menos-de-15-dias.html'

# ======================================================================================================================
# ======================================================================================================================
# FILTER CONFIGS

path_map_barrios = './utils/maps/barrios.shp'
lista_barrios = './utils/filters/barrios.csv'

barrios_dict = './utils/filters/barrios_dict.json'
manantiales_tipos = './utils/filters/manantiales_tipos.json'

path_df_LV = '../Data/Fuentes/LV/df_LV.csv'
path_df_ML = '../Data/Fuentes/ML/df_ML.csv'
path_df_ZP = '../Data/Fuentes/ZP/df_ZP.csv'

# ======================================================================================================================
# ======================================================================================================================
# ANALYSIS CONFIGS

path_reports = '../Data/Reportes/'
path_unify = '../Data/Unificadas/'
ciudades = ["CORDOBA", "LA CALERA", "MALAGUENO", "MENDIOLAZA", "RIO CEBALLOS", 
             "VILLA ALLENDE", "VILLA CARLOS PAZ"]