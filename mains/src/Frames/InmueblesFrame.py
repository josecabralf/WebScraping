import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class InmueblesFrame:
  _tipos_datos = {
    "id": "object",
    "tipoPropiedad": "object",
    "precioUSD": 'int64',
    "fechaUltimaActualizacion": "object",
    "vendedor": "object",
    "terrenoTotal": 'float64',
    "terrenoEdificado": 'float64',
    "cantDormitorios": 'float64',
    "cantBanos": 'float64',
    "cantCochera": 'float64',
    "barrio": "object",
    "ciudad": "object",
    "coordX": 'float64',
    "coordY": 'float64',
    "URL": 'object'}
  
  def __init__(self, path: str = None, col: str = None, df: pd.DataFrame = pd.DataFrame()) -> None:
    if path and os.path.isfile(path): self._df = self.abrir_df(path, col)
    else: self._df = df
    
  def get_df(self) -> pd.DataFrame: return self._df
  def set_df(self, df) -> None: self._df = df
  
  def get_activos(self, limit = 45) -> pd.DataFrame:
    hoy = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    self._df['fechaUltimaActualizacion'] = pd.to_datetime(self._df['fechaUltimaActualizacion'], format='%Y-%m-%d')
    activos = self._df.loc[(hoy - self._df['fechaUltimaActualizacion']) <= timedelta(days=limit)]
    return activos
  
  def abrir_df(self, path: str, col: str):
    if not col: return pd.read_csv(path, sep=';', dtype=self._tipos_datos)
    return pd.read_csv(path, sep=';', index_col=col, dtype=self._tipos_datos)
    
  def guardar_df(self, archivo, excel = False, activos = False):
    save_df = self._df
    if activos: save_df = self.get_activos()
    if excel: save_df.to_excel(archivo, index=False)
    else: save_df.to_csv(archivo, index=False, sep=';')
  
  def concat(self, list_frames : list): 
    for frame in list_frames:
      if isinstance(frame, pd.DataFrame): self._append_df(frame)
      elif isinstance(frame, InmueblesFrame): self._append_frame(frame)
      else: print("Warning: one of the elements provided was not a DataFrame or a Frame. It will be ignored.")
      
  def _append_df(self, df): self._df = self._df._append(df, ignore_index=True)
  def _append_frame(self, frame): self._df = self._df._append(frame.get_df(), ignore_index=True)
  
  def replace_column(self, column: str, replacements:dict):
    try: self._df.loc[:, column] = self._df.loc[:, column].replace(replacements)
    except KeyError: print("Error: the column provided does not exist in the DataFrame.")
    except TypeError: print("Error: the replacements provided are not a dictionary.")
  
  def format(self): self.set_df(self.CommandFormat().format_frame(self._df))
  
  def get_filt_barrios_raros(self, n=5):
    value_counts = self._df['barrio'].value_counts()
    barrios_raros = value_counts[value_counts < n].index
    filt = self._df['barrio'].isin(barrios_raros)
    return filt
  
  def replace_values_filt(self, filt, df_reemplazo: pd.DataFrame):
    try: self._df.loc[filt] = df_reemplazo
    except: print("Error: the replacements provided has different indexes.")
    
  def reemplazar_tipo_prop_segun_barrio(self, diccionario):
    self._df.loc[:, 'tipoPropiedad'] = self._df.loc[:, 'barrio'].map(diccionario).fillna(self._df.loc[:, 'tipoPropiedad'])
    self._df.loc[(self._df['tipoPropiedad'] == 'CASA') & 
                 self._df['terrenoEdificado'].isna(), 'tipoPropiedad'] = 'TERRENO'
    self._df.loc[(self._df['tipoPropiedad'] == 'DEPARTAMENTO') & 
                 self._df['terrenoEdificado'].isna(), 'tipoPropiedad'] = 'TERRENO'
  
  class CommandFormat:
    def format_frame(self, df) -> pd.DataFrame:
        df['fechaUltimaActualizacion'] = pd.to_datetime(df['fechaUltimaActualizacion'], format='%Y-%m-%d')
        df['fechaUltimaActualizacion'] = df['fechaUltimaActualizacion'].apply(self.corregir_fecha)
        df = self.cambiar_valores_null(df)
        df = self.eliminar_duplicados_id(df)
        df = self.eliminar_duplicados_coords(df)
        df = self.eliminar_terrenos_nulos(df)
        return df

    def cambiar_valores_null(self, df): return df.replace(-1, np.nan)

    def corregir_fecha(self, fecha):
        if fecha > datetime.today(): return fecha.replace(day=fecha.month, month=fecha.day).strftime("%Y-%m-%d")
        return fecha.strftime("%Y-%m-%d")

    def eliminar_duplicados_id(self, df):
        df.sort_values(by='fechaUltimaActualizacion', ascending=True, inplace=True)
        return df.drop_duplicates(subset='id', keep='last', ignore_index=False)
      
    def eliminar_duplicados_coords(self, df):
        df.sort_values(by='fechaUltimaActualizacion', ascending=True, inplace=True)
        return df.drop_duplicates(subset=['coordX', 'coordY', 'precioUSD'], keep='last', ignore_index=False)

    def eliminar_terrenos_nulos(self, df): return df.dropna(how="all", subset=['terrenoTotal', 'terrenoEdificado'])