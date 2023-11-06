from src.Scrapers.Publicacion import Publicacion
from src.Scrapers.SoupStrategy import SoupStrategy
from unidecode import unidecode
from datetime import datetime
import re

class PublicacionLV(Publicacion):
    def __init__(self, url: str, strategy_soup: SoupStrategy, 
                 hoy: datetime = datetime.today(), fecha_c: datetime = None):
        self._fecha_corte = fecha_c
        super().__init__(url, strategy_soup, hoy)
    
    def find_id(self) -> str: return self._url.split('/')[5]
        
    def find_precio(self) -> int:
        try:
            precio = self.soup.find('div', class_='h2 mt0 main bolder').text.strip().split()
            if precio[0] == 'U$S':
                precio = int(precio[1].replace('.', ''))
                return precio
        except AttributeError as err:
            self.crear_log_error('No se pudo obtener precio de publicacion. Revisar get_precio()', err)
        return 0

    def find_fecha(self, hoy:datetime) -> str: 
        try:
            fecha = self.soup.find('div', class_='h5 center').text.split(':')[1].strip().replace('.', '-')
            fecha = datetime.strptime(fecha, "%d-%m-%Y")
            if self._fecha_corte and fecha < self._fecha_corte: return ''
            elif (hoy - fecha).days > 45: return ''
            return datetime.strftime(fecha, "%Y-%m-%d")
        except Exception as err:
            self.crear_log_error('No se pudo obtener fecha de publicacion. Revisar find_fecha()', err)
            return ''

    def find_vendedor(self) -> str:
        datos = self.soup.find('div', class_='clearfix px1 py1')
        try:
            tipoVendedor = datos.find('h4', class_='m0').text.strip().upper()
            tipoVendedor = unidecode(re.sub(' +', ' ', tipoVendedor))
        except: tipoVendedor = 'PARTICULAR'
        return tipoVendedor

    def find_coord(self) -> list:
      try:
        img = self.soup.find('amp-iframe', id='map-iframe')['src']
        loc = img.split('marker=')[1]
        return [float(n) for n in loc.split('%2C')]
      except: return [None, None]
      
    class CommandCaracteristicas(Publicacion.CommandCaracteristicas):
        def execute(self,publicacion: Publicacion) -> dict:
            caracteristicas = publicacion.soup.find_all('div', class_='flex-auto nowrap col-4')
            try:
                caracteristicas = [car.text.strip().split() for car in caracteristicas]
                datos_interes = self.get_caracteristicas(caracteristicas, publicacion.url)
            except TypeError as err:
                publicacion.crear_log_error('No se pudieron obtener caracteristicas de publicacion. Revisar CommandCaracteristicas', err)
                return False
            return {
                    "tipo" : datos_interes[0],
                    "TT" : datos_interes[1],
                    "TE" : datos_interes[2],
                    "Dorms" : datos_interes[3],
                    "Banos" : datos_interes[4],
                    "Cocheras" : datos_interes[5],
                    "Barrio" : datos_interes[6],
                    "Ciudad" : datos_interes[7] 
                    }
                
        def get_caracteristicas(self, caracteristicas, url) -> dict:
            deseados = {'Tipo vivienda': url.split('/')[4].replace('-',' ').upper(),
                        'Superficie total': -1,
                        'Superficie cubierta': -1,
                        'Dormitorios': -1,
                        'Baños': -1,
                        'Cocheras': -1,
                        'Barrio': '',
                        'Ciudad': ''}

            flag_superficie, flag_ubicacion = False, False

            for dato in caracteristicas:
                if dato[0] == 'FichaInmueble_tipovivienda': deseados['Tipo vivienda'] = str(dato[1]).upper()
                elif dato[0] == 'FichaInmueble_superficie':
                    if not flag_superficie:
                        self.asignar_superficie(deseados, dato, 'Superficie total')
                        flag_superficie = True
                    else: self.asignar_superficie(deseados, dato, 'Superficie cubierta')
                elif dato[0] == 'fichaproductos_ciudad':
                    if not flag_ubicacion:
                        self.asignar_ubicacion(deseados, dato, 'Ciudad')
                        flag_ubicacion = True
                    else: self.asignar_ubicacion(deseados, dato, 'Barrio')
                elif dato[0] == 'FichaInmueble_dormitorios':
                    self.asignar_dato_variable(deseados, dato, 'Dormitorios')
                elif dato[0] == 'FichaInmueble_bano':
                    self.asignar_dato_variable(deseados, dato, 'Baños')
                elif dato[0] == 'menu_vehiculos':
                    self.asignar_dato_variable(deseados, dato, 'Cocheras')
            return [
                deseados['Tipo vivienda'],
                deseados['Superficie total'],
                deseados['Superficie cubierta'],
                deseados['Dormitorios'],
                deseados['Baños'],
                deseados['Cocheras'],
                deseados['Barrio'],
                deseados['Ciudad']
            ]

        def asignar_superficie(self, diccionario, arreglo, clave) -> None:
            try: diccionario[clave] = int(round(float(arreglo[1]), 0))
            except: diccionario[clave] = int(round(float(arreglo[1].replace(',', '.').split('m')[0])))

        def asignar_ubicacion(self, diccionario, arreglo, clave) -> None:
            diccionario[clave] = unidecode((' '.join(arreglo[1:len(arreglo)+1])).upper())

        def asignar_dato_variable(self, diccionario, arreglo, clave) -> None:
            for j in range(1, len(arreglo)):
                try: diccionario[clave] = int(arreglo[j])
                except: continue
                break