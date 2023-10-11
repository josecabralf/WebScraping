from Scrapers.Publicacion.Publicacion import Publicacion
from Scrapers.CaracteristicasStrategy import CaracteristicasStrategy
from Scrapers.SoupStrategy import SoupStrategy
from datetime import timedelta, datetime

class PublicacionML(Publicacion):
  def __init__(self, url: str, strategy_soup: SoupStrategy, strategy_caract: CaracteristicasStrategy, hoy: datetime = datetime.today(), ubic: list = [None, None]):
    super().__init__(url.split('#')[0], strategy_soup, strategy_caract, hoy)
    if (ubic[0] and ubic[1]) and not (self._caracteristicas['Ciudad'] or self._caracteristicas['Barrio']):
      self._caracteristicas['Ciudad'] = ubic[0]
      self._caracteristicas['Barrio'] = ubic[1]
  
  def find_id(self) -> str: 
      return self._url.split('-')[1]
    
  def find_precio(self) -> int:
    try:
        precio = self.soup.find('span', class_='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact').find(
            'span', class_='andes-visually-hidden').text.split()
        if precio[1] == 'dólares':
            precio = int(precio[0])
            return precio
        else:
            return 0
    except AttributeError as err:
        self.crear_log_error('No se pudo obtener precio de publicacion. Revisar get_precio()', err)
        return 0
  
  def find_fecha_activo(self, hoy) -> tuple:
    delta = None
    try:
        try:
            dias_desde_actualiz = self.soup.find('p', class_='ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle').text.split()
        except:
            dias_desde_actualiz = self.soup.find('p', class_='ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller-validated__title').text.split()
        if dias_desde_actualiz[3] in ["día", "días"]: delta = int(dias_desde_actualiz[2])
        elif dias_desde_actualiz[3] in ["mes"]: delta = int(dias_desde_actualiz[2]) * 31
        elif dias_desde_actualiz[3] in ["meses", "año", "años"]: return '', False
        if delta==None or delta > 45: return '', False
        fecha = (hoy - timedelta(days=delta)).strftime("%Y-%m-%d")
        return fecha, True
    except Exception as err:
        self.crear_log_error(f'No se pudo obtener fecha de publicacion. Revisar get_fecha_activo(). {self._url}', err)
        return '', False
  
  def find_vendedor(self) -> str:
    try:
        vendedor = self.soup.find('div', id='seller_profile').find('h2').text.upper().split()[-1]
        if vendedor != 'PARTICULAR': return 'INMOBILIARIA'
        return vendedor
    except: return 'INMOBILIARIA'

  def find_coord(self) -> list:
    i = 1
    coord = self.get_datos_coord()
    while not coord[0]:
      coord = self.get_datos_coord()
      if i >= 5 and not coord[0]: 
        self.agregar_revision()
        return [None, None]
      i += 1
      self.set_soup()
    return coord
            
  def get_datos_coord(self):
    try:
        ubic = self.soup.find('div', class_='ui-vip-location')
        img = ubic.find('img')['src']
        loc = img.split('&')[4].split('=')[1]
        if loc: return [float(n) for n in loc.split('%2C')]
    except: return [None, None]