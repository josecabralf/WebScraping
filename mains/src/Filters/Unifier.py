import json
from src.Singleton import Singleton
from config import barrios_dict, manantiales_tipos, ciudades
from src.Frames.InmueblesFrameHandler import InmueblesFrameHandler
from src.Filters.Correctors.Corrector import Corrector


class Unifier(Singleton):
  _barrios_dict = barrios_dict
  _manantiales_tipos = manantiales_tipos
  _ciudades = ciudades
  def __init__(self) -> None:
    self.set_frame()
    self._corrector = Corrector()
        
  def execute(self):
    self.reemplazar_estandares()
    self.filtrar_patrones()
    self.filtrar_coordenadas()
    self.filtrar_fuzzy()
    self.eliminar_restantes()
    self.reemplazar_manantiales()
  
  def reemplazar_estandares(self):
    with open(barrios_dict, 'r', encoding='utf-8') as f: diccionario = json.load(f)
    self._frame.replace_column('barrio', diccionario)
    
  def filtrar_patrones(self):
    df = self._corrector.filtrar_patrones(self.get_df())
    self._frame.set_df(df)
    self.reemplazar_estandares()
    
  def filtrar_coordenadas(self):
    filt = self._frame.get_filt_barrios_raros()
    df = self._corrector.filtar_coordenadas(self.get_df().loc[filt])
    self._frame.replace_values_filt(filt, df)
    self.reemplazar_estandares()
    
  def filtrar_fuzzy(self):
    filt = self._frame.get_filt_barrios_raros()
    df = self._corrector.filtrar_fuzzy(self.get_df().loc[filt])
    self._frame.replace_values_filt(filt, df)
    self.reemplazar_estandares()
    
  def eliminar_restantes(self):
    df = self.get_df()
    filt = ((df['barrio'].isin(['SD', 'OTRO', 'OTROS', '0'])) | 
            (df['barrio'].str.contains('CASA')) |
            df['barrio'].str.contains('DEPARTAMENTO') |
            df['barrio'].str.contains('DUPLEX') |
            df['barrio'].str.contains('TERRENO') |
            df['barrio'].str.contains('LOTE'))
    self._frame.set_df(df.loc[~filt])
  
  def reemplazar_manantiales(self):
    df = self.get_df()
    filt = (df['barrio'] == "MANANTIALES") | (df['barrio'] == "MANANTIALES II")
    df.loc[filt,"barrio"] = df.loc[filt].apply(lambda x: self._corregir_barrio_manantiales(x['URL'], x['barrio']), axis=1)
    self._frame.set_df(df)
    filt = self._frame.get_filt_barrios_raros(n=3)
    self._frame.set_df(self.get_df().loc[~filt])
    self.corregir_tipo_manantiales()
    self.reemplazar_estandares()
    
  def _corregir_barrio_manantiales(self, url, barrio):
    dato = url.split('/')[-1].replace('-', ' ').upper()
    dato = self._corrector.busqueda_manantiales(dato)
    if dato.__contains__("MANANTIALES") and len(dato.split()[0])> 4 and (dato.split()[0]!='ATRAS'): return dato
    else:
        search = self._corrector.busqueda_fuzz(dato)
        if search != dato: return search
    return barrio
  
  def corregir_tipo_manantiales(self):
    with open(manantiales_tipos, 'r', encoding='utf-8') as f: diccionario = json.load(f)
    self._frame.reemplazar_tipo_prop_segun_barrio(diccionario)
  
  def set_frame(self): 
    self._frame = InmueblesFrameHandler().open_frames()
    df = self.get_df()
    self._frame.set_df(df.loc[df['ciudad'].isin(self._ciudades), "tipoPropiedad":"URL"])
  def get_frame(self): return self._frame  
  
  def get_df(self): return self._frame.get_df()