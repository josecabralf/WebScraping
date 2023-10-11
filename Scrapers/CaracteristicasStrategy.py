from unidecode import unidecode
from abc import abstractmethod
from Scrapers.Logger import Loggeable


class CaracteristicasStrategy(Loggeable):
    _instance = None
    @classmethod
    def get_instance(self):
        if self._instance is None:
            self._instance = self()
        return self._instance
    @abstractmethod
    def execute(self,publicacion) -> dict:
        pass


class CaracteristicasStrategyLV(CaracteristicasStrategy):
    def execute(self,publicacion) -> dict:
        caracteristicas = publicacion.soup.find_all('div', class_='flex-auto nowrap col-4')
        try:
            caracteristicas = [car.text.strip().split() for car in caracteristicas]
            datos_interes = self.get_caracteristicas(caracteristicas, publicacion.url)
        except TypeError as err:
            self.crear_log_error('No se pudieron obtener caracteristicas de publicacion. Revisar get_caracteristicas()', err)
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


class CaracteristicasStrategyML(CaracteristicasStrategy):
    def execute(self,publicacion) -> dict:
        tipo = (publicacion.url.split('.')[0].split('//')[1]).upper()
        try:
            datos_interes = self.get_caracteristicas(publicacion,tipo)
            barrio, ciudad = self.get_ubicacion(publicacion)
        except TypeError as err:
            self.crear_log_error('No se pudieron obtener caracteristicas de publicacion. Revisar get_caracteristicas()', err)
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
        if caracteristicas: return self.get_list_caracteristicas(caracteristicas)
        return False

    def get_caracteristicas(self, publicacion, tipo_prop: str) -> list:
        if tipo_prop == "TERRENO": return self.get_caracteristicas_terreno(publicacion)
        return self.get_caracteristicas_inmueble(publicacion)

    def get_list_caracteristicas(self,caracteristicas) -> list:
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

      
class CaracteristicasStrategyZP(CaracteristicasStrategy):
    def execute(self,publicacion) -> dict:
        try:
            caracteristicas = [car.text.strip() for car in publicacion.soup.find_all('li', class_="icon-feature")]
            caracteristicas = self.get_datos_caracteristicas(caracteristicas)
            tipo, ciudad, barrio = self.get_tipo_y_ubicacion(publicacion)
        except TypeError as err:
            self.crear_log_error('No se pudo obtener las caracteristicas de la publicacion. Revisar get_caracteristicas()', err)
            return False
        
        return {
            "tipo" : tipo,
            "TT" : caracteristicas[0],
            "TE" : caracteristicas[1],
            "Dorms" : caracteristicas[2],
            "Banos" : caracteristicas[3],
            "Cocheras" : caracteristicas[4],
            "Barrio" : barrio,
            "Ciudad" : ciudad
        }
    
    def get_tipo_y_ubicacion(self, publicacion):
        ubicacion = publicacion.soup.find_all('a', class_="bread-item-redirect")
        tipo_prop = ubicacion[1].text.strip().upper()
        try:
            ciudad = unidecode(ubicacion[4].text.strip().upper())
            barrio = unidecode(ubicacion[5].text.strip().upper())
            del ubicacion
        except: return None, None, None
        return tipo_prop, ciudad, barrio
    
    def get_datos_caracteristicas(self, caracteristicas):
        deseados = {'m² tot.': -1,
                    'm² cub.': -1,
                    'dorm.': -1,
                    'Baños': -1,
                    'coch.': -1}
        for car in caracteristicas:
            car = car.split('\n')
            try:
                if car[1] in deseados: deseados[car[1]] = float(car[0])
                elif car[1][-1] != 's':
                    car[1] = car[1] + 's'
                    if car[1] in deseados: deseados[car[1]] = float(car[0])
            except: continue
        return [
            deseados['m² tot.'],
            deseados['m² cub.'],
            deseados['dorm.'],
            deseados['Baños'],
            deseados['coch.']
        ]