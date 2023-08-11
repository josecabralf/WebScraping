# Escritura de archivos
cols = 'id;tipoPropiedad;precioUSD;fechaUltimaActualizacion;tipoVendedor;terrenoTotal;terrenoEdificado;cantDormitorios;cantBanos;cantCochera;barrio;ciudad;coordX;coordY;activo;URL\n'

# LaVoz
URL_LaVoz = 'https://clasificados.lavoz.com.ar/inmuebles/todo?provincia=cordoba&operacion=venta'
archivos_LaVoz = './results/LV/'
archivo_fecha = './utils/fechaUltimoScrap.txt'

# MercadoLibre
archivos_Links = './utils/links_ML/links.txt'
leidos_links = './utils/links_ML/leidos.txt'
errores_links = './utils/links_ML/errores.txt'
publicadosHoy = './utils/links_ML/hoy.txt'
archivos_Meli = './results/ML/'

URL_Meli_CASAS = 'https://inmuebles.mercadolibre.com.ar/casas/venta/propiedades-individuales/cordoba/inmuebles_NoIndex_True'
URL_Meli_DPTOS = 'https://inmuebles.mercadolibre.com.ar/departamentos/venta/propiedades-individuales/cordoba/inmuebles_NoIndex_True'
URL_Meli_TERS = 'https://inmuebles.mercadolibre.com.ar/terrenos-lotes/venta/propiedades-individuales/cordoba/inmuebles_NoIndex_True'

# Zonaprop
URL_ZonaProp = 'https://www.zonaprop.com.ar/casas-departamentos-ph-terrenos-venta-cordoba.html'
URL_Base = 'https://www.zonaprop.com.ar'

archivos_filtros = './utils/links_ZP/filtros.txt'
publicados_recientes = './utils/links_ZP/ultima_semana.txt'
archivos_ZonaProp = './results/ZP/'
revisionesFecha = './utils/links_ZP/revisiones/revisionesFecha.txt'

path_driver = "./utils/driver/chromedriver"
