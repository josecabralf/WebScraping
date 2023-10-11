from Scrapers.Publicacion.Publicacion import Publicacion
from Scrapers.CaracteristicasStrategy import CaracteristicasStrategy
from Scrapers.SoupStrategy import SoupStrategy
from datetime import timedelta, datetime

class PublicacionZP(Publicacion):
  def __init__(self, url: str, strategy_soup: SoupStrategy, strategy_caract: CaracteristicasStrategy, hoy: datetime = datetime.today()):
    super().__init__(url, strategy_soup, strategy_caract, hoy)
  
  def find_id(self) -> str: return self._url.split('-')[-1].split('.')[0]
    
  def find_precio(self) -> int:
    try:
        precio = self.soup.find('div', class_='price-value').find('span').find('span').text.split()
        if precio[0] == 'USD':
            precio = int(precio[1].replace('.', ''))
            return precio
        else: return 0
    except AttributeError as err:
        self.crear_log_error('No se pudo obtener precio de publicacion. Revisar get_precio()', err)
        return 0
  
  def find_fecha_activo(self, hoy) -> tuple: 
    try:
        delta = self.soup.find('div', id='user-views').find('p').text.split()
        if not delta: self.agregar_revision()
        if delta[-1] == 'hoy': delta = 0
        elif delta[-1] == 'ayer': delta = 1
        elif delta[-1] in ['día', 'días']: delta = int(delta[-2])
        elif delta[-1] in ['mes']: delta = 31*int(delta[-2])
        elif delta[-1] in ['meses', 'año', 'años',]: return '', False

        fecha = hoy - timedelta(days=delta)
        fecha = fecha.strftime("%Y-%m-%d")
        return fecha, True
    except Exception as err:
        self.crear_log_error('No se pudo obtener fecha de publicacion. Revisar get_fecha_activo()', err)
        return '', False
  
  def find_vendedor(self) -> str:
    vendedor = self.soup.find('div', class_='feature-info')
    if vendedor: return 'PARTICULAR'
    return 'INMOBILIARIA'

  def find_coord(self) -> list:
    try:
        mapa = self.soup.find('img', id="static-map")["src"]
        loc = mapa.split('?')[1].split('&')[0].split('=')[1]
        return [float(n) for n in loc.split(',')]
    except:
        self.crear_log_error('No se pudo obtener coords de publicacion. Revisar get_coord()')
        return [None, None]