from Scrapers.Publicacion.Publicacion import Publicacion
from Scrapers.CaracteristicasStrategy import CaracteristicasStrategy
from Scrapers.SoupStrategy import SoupStrategy
from datetime import datetime

class PublicacionLV(Publicacion):
    def __init__(self, url: str, strategy_soup: SoupStrategy, strategy_caract: CaracteristicasStrategy, 
                 hoy: datetime = datetime.today(), fecha_c: datetime = None):
        self._fecha_corte = fecha_c
        super().__init__(url, strategy_soup, strategy_caract, hoy)
    
    def find_id(self) -> str: return self._url.split('/')[5]
        
    def find_precio(self) -> int:
        try:
            precio = self.soup.find('div', class_='h2 mt0 main bolder').text.strip().split()
            if precio[0] == 'U$S':
                precio = int(precio[1].replace('.', ''))
                return precio
            else: return 0
        except AttributeError as err:
            self.crear_log_error('No se pudo obtener precio de publicacion. Revisar get_precio()', err)
            return 0

    def find_fecha_activo(self, hoy) -> tuple: 
        try:
            fecha = self.soup.find('div', class_='h5 center').text.split(':')[1].strip().replace('.', '-')
            fecha = datetime.strptime(fecha, "%d-%m-%Y")
            if self._fecha_corte:
                if fecha < self._fecha_corte: return '', False
            delta = hoy - fecha
            if delta.days > 45: return '', False
            return datetime.strftime(fecha, "%Y-%m-%d"), True
        except Exception as err:
            self.crear_log_error('No se pudo obtener fecha de publicacion. Revisar get_fecha_activo()', err)
            return '', False

    def find_vendedor(self) -> str:
        datos = self.soup.find('div', class_='clearfix px1 py1')
        try: tipoVendedor = datos.find('div', class_='h5 gray').text.strip().upper()
        except:tipoVendedor = 'PARTICULAR'
        return tipoVendedor

    def find_coord(self) -> list:
      try:
        img = self.soup.find('amp-iframe', id='map-iframe')['src']
        loc = img.split('marker=')[1]
        return [float(n) for n in loc.split('%2C')]
      except: return [None, None]