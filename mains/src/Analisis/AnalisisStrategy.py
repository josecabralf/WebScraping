import pandas as pd
from src.Singleton import Singleton
from abc import abstractmethod

class AnalisisStrategy(Singleton):
  @abstractmethod
  def execute(self, df): pass

class AnalisisStrategyPM2(AnalisisStrategy):
  def execute(self, df) -> pd.DataFrame:
    self._agregar_columnas_pm2(df)
    barrios = self._agrupar_por_barrio(df)
    tipo_prop = self.get_tipo_propiedad(df)
    resultados = self._calcular_estadisticas_inmuebles(barrios, tipo_prop)
    resultados.rename(columns={'ciudad':'Ciudad', 'barrio': 'Barrio'}, inplace=True)
    return resultados
  
  def _calcular_estadisticas_inmuebles(self, barrios, tipo_prop):
    if tipo_prop == 'CASA':
        res = self._calcular_datos_por_tipo_terreno(barrios, 'edificado')
        res['T Total Prom'] = barrios['terrenoTotal'].mean().round(1)
    elif tipo_prop == 'DEPARTAMENTO': res = self._calcular_datos_por_tipo_terreno(barrios, 'edificado')
    else: res = self._calcular_datos_por_tipo_terreno(barrios, 'total')
    res.reset_index(inplace=True)
    return res

  def _calcular_datos_por_tipo_terreno(self, barrios, tipo_terreno):
    precio_m2_prom = barrios[f'$/m2_{tipo_terreno}'].mean().round(1)
    min = barrios[f'$/m2_{tipo_terreno}'].min().round(1)
    max = barrios[f'$/m2_{tipo_terreno}'].max().round(1)
    return pd.DataFrame({'Cantidad': barrios.size(),
                          'Terreno Promedio': barrios[f'terreno{tipo_terreno.capitalize()}'].mean().round(1),
                          'Precio Promedio': barrios['precioUSD'].mean().round(1),
                          'Promedio $/m2': precio_m2_prom,
                          'Mediana $/m2': barrios[f'$/m2_{tipo_terreno}'].median().round(1),
                          'Minimo $/m2': min,
                          'Maximo $/m2': max,
                          'Rango %': (((max - min)/precio_m2_prom)*100).round(1)})
  
  def _agrupar_por_barrio(self, df: pd.DataFrame):
    filt = (df["ciudad"] != "CORDOBA") & (df["barrio"] == "CENTRO")
    df.loc[filt, "barrio"] = "CENTRO " +  df.loc[filt, "ciudad"]
    barrios = df.groupby(['barrio'])
    return barrios
  
  def _agregar_columnas_pm2(self, df: pd.DataFrame):
    pd.options.mode.chained_assignment = None
    df.loc[:, '$/m2_total'] = df['precioUSD'] / df['terrenoTotal']
    df['$/m2_edificado'] = df['precioUSD'] / df['terrenoEdificado']
    pd.options.mode.chained_assignment = 'warn'
    
  def get_tipo_propiedad(self, df): return df['tipoPropiedad'].unique()[0]