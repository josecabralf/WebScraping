from src.Scrapers.Publicacion import Publicacion
from src.Scrapers.SoupStrategy import SoupStrategy
from datetime import timedelta, datetime
from unidecode import unidecode

class PublicacionML(Publicacion):
  def __init__(self, url: str, strategy_soup: SoupStrategy, hoy: datetime = datetime.today(), ubic: list = [None, None]):
    super().__init__(url.split('#')[0], strategy_soup, hoy)
    if (ubic[0] and ubic[1]) and not (self._caracteristicas['Ciudad'] or self._caracteristicas['Barrio']):
      self._caracteristicas['Ciudad'] = ubic[0]
      self._caracteristicas['Barrio'] = ubic[1]
  
  def find_id(self) -> str: 
      return self._url.split('-')[1]
    
  def find_precio(self) -> int:
    try:
        precio = self.soup.find('span', class_='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact').find(
            'span', class_='andes-visually-hidden').text.split()
        if precio[1] == 'dólares': return int(precio[0])
    except AttributeError as err:
        self.crear_log_error('No se pudo obtener precio de publicacion. Revisar get_precio()', err)
    return 0
  
  def find_fecha(self, hoy) -> str:
    delta = None
    try:
      try: dias_desde_actualiz = self.soup.find('p', class_='ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-header__bottom-subtitle').text.split()
      except: dias_desde_actualiz = self.soup.find('p', class_='ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller-validated__title').text.split()
            
      if dias_desde_actualiz[3] in ["día", "días"]: delta = int(dias_desde_actualiz[2])
      elif dias_desde_actualiz[3] in ["mes"]: delta = int(dias_desde_actualiz[2]) * 31
      elif dias_desde_actualiz[3] in ["meses", "año", "años"]: return ''
      
      if not delta: 
        self.agregar_revision()
        return ''
      elif delta > 45: return ''
        
      fecha = (hoy - timedelta(days=delta)).strftime("%Y-%m-%d")
      return fecha
      
    except Exception as err:
      self.crear_log_error(f'No se pudo obtener fecha de publicacion. Revisar get_fecha().', err)
      self.agregar_revision()
      return ''
  
  def find_vendedor(self) -> str:
    datos = self.soup.find('div', id='seller_profile')
    try:
        tipo = datos.find('h2').text.upper().split()[-1]
        if tipo != 'PARTICULAR': 
            try: 
              nom = datos.find('h3').text.upper()
              return nom
            except Exception as e: 
              self.crear_log_error('No se pudo obtener nombre de inmobiliaria. Revisar find_vendedor().', e)
              return 'INMOBILIARIA'
        return 'PARTICULAR'
    except Exception as err: 
      self.crear_log_error('No se pudo obtener tipo de vendedor de publicacion. Revisar find_vendedor().', err)
      return ''

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
    
  class CommandCaracteristicas(Publicacion.CommandCaracteristicas):
    def execute(self,publicacion: Publicacion) -> dict:
        tipo = (publicacion.url.split('.')[0].split('//')[1]).upper()
        try:
            datos_interes = self.get_caracteristicas(publicacion,tipo)
            barrio, ciudad = self.get_ubicacion(publicacion)
        except TypeError as err:
            publicacion.crear_log_error('No se pudieron obtener caracteristicas de publicacion. Revisar CommandCaracteristicas', err)
            return False
        if not datos_interes: return False
        return {
                "tipo" : tipo,
                "TT" : datos_interes[0],
                "TE" : datos_interes[1],
                "Dorms" : datos_interes[2],
                "Banos" : datos_interes[3],
                "Cocheras" : datos_interes[4],
                "Barrio" : barrio,
                "Ciudad" : ciudad 
                }
        
    def get_caracteristicas_terreno(self, publicacion) -> list:
        i = 1
        terreno = self.buscar_terreno(publicacion)
        while not terreno:
            publicacion.set_soup()
            terreno = self.buscar_terreno(publicacion)
            if i >= 5 and not terreno: return False
            i += 1
        return [terreno, -1, -1, -1, -1]
    
    def buscar_terreno(self, publicacion) -> int:
        terreno = publicacion.soup.find("span", class_="ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-label")
        if terreno: return int(round(float(terreno.text.split()[0]), 0))
        return False
    
    def get_caracteristicas_inmueble(self, publicacion) -> list:
        i = 1
        caracteristicas = self.buscar_inmueble(publicacion)
        while not caracteristicas:
            publicacion.set_soup()
            caracteristicas = self.buscar_inmueble(publicacion)
            if i == 5 and not caracteristicas: return False
            i += 1
        return caracteristicas
    
    def buscar_inmueble(self, publicacion):
        caracteristicas = publicacion.soup.find("tbody", class_="andes-table__body")
        if caracteristicas: return self.get_list_caracteristicas_inmueble(caracteristicas)
        return False

    def get_caracteristicas(self, publicacion, tipo_prop: str) -> list:
        if tipo_prop == "TERRENO": return self.get_caracteristicas_terreno(publicacion)
        return self.get_caracteristicas_inmueble(publicacion)

    def get_list_caracteristicas_inmueble(self,caracteristicas) -> list:
        headers = caracteristicas.find_all('th')
        body = caracteristicas.find_all('td')
        deseados = {'Superficie total': -1,
                    'Superficie cubierta': -1,
                    'Dormitorios': -1,
                    'Baños': -1,
                    'Cocheras': -1}
        for i in range(len(headers)):
            car = headers[i].text
            if car in deseados:
                val = body[i].text.split()[0]
                try: deseados[car] = int(val)
                except: deseados[car] = int(round(float(val), 0))
        return [
            deseados['Superficie total'],
            deseados['Superficie cubierta'],
            deseados['Dormitorios'],
            deseados['Baños'],
            deseados['Cocheras']
        ]
      
    def get_ubicacion(self, publicacion):
        ciudad, barrio = None, None
        try:
            ubicacion = publicacion.soup.find_all('a', class_='andes-breadcrumb__link')
            ciudad, barrio = unidecode(ubicacion[5].text.upper()), unidecode(ubicacion[6].text.upper())
        except: barrio = publicacion.soup.find('h1').text.upper()
        return barrio, ciudad
