from abc import abstractmethod
from src.Frames.InmueblesFrame import InmueblesFrame
import pandas as pd
import numpy as np
from src.Singleton import Singleton


class StrategyFilter(Singleton):      
    def gral_filter(self, frame: InmueblesFrame): 
      frame.set_df(self.specific_gral_filter(frame.get_df()))
    
    @abstractmethod
    def specific_gral_filter(self, df: pd.DataFrame) -> pd.DataFrame: ...
    
    def property_filter(self, frame: InmueblesFrame) -> InmueblesFrame: 
      df = frame.get_df()
      terrenos = self.terrenos_filter(df.loc[df["tipoPropiedad"] == "TERRENO"])
      deptos = self.deptos_filter(df.loc[df["tipoPropiedad"] == "DEPARTAMENTO"])
      casas = self.casas_filter(df.loc[df["tipoPropiedad"] == "CASA"])
      frame.set_df(pd.concat([terrenos, deptos, casas], ignore_index=True))

    @abstractmethod
    def terrenos_filter(self, terrenos: pd.DataFrame) -> pd.DataFrame: ...
    @abstractmethod
    def deptos_filter(self, deptos: pd.DataFrame) -> pd.DataFrame: ...
    @abstractmethod
    def casas_filter(self, casas: pd.DataFrame) -> pd.DataFrame: ...
      
      
class FilterLV(StrategyFilter):
  def specific_gral_filter(self, df: pd.DataFrame) -> pd.DataFrame:
    reemplazos = {
        "DUPLEX" : "CASA",
        "DÚPLEX" : "CASA",
        "TRIPLEX" : "CASA",
        "CHALET" : "CASA", 
        "PREFABRICADA": "CASA", 
        "CABAÑA" : "CASA",
        "SEMIPISO" : "DEPARTAMENTO",
        "PISO" : "DEPARTAMENTO",
        "PENTHOUSE" : "DEPARTAMENTO",
        "LOFT" : "DEPARTAMENTO",
        "TERRENOS LOTES" : "TERRENO"
    }
    df["tipoPropiedad"].replace(reemplazos, inplace= True)

    filt = (df["tipoPropiedad"] == "CASA") | (df["tipoPropiedad"] == "DEPARTAMENTO") | (df["tipoPropiedad"] == "TERRENO")
    df = df.loc[filt]
    
    df = df.loc[~((df['terrenoEdificado'] == 1) | 
                  (df['terrenoEdificado'] == 1) |
                  (df['precioUSD'] == 1))]
    return df
  
  def terrenos_filter(self, terrenos: pd.DataFrame) -> pd.DataFrame: 
    filtro_P = terrenos["precioUSD"].between(1500, 1000000)
    filtro_T = (terrenos['terrenoTotal'].between(50, terrenos['terrenoTotal'].quantile(0.995)))
    return terrenos.loc[filtro_P & filtro_T]
  
  def deptos_filter(self, deptos: pd.DataFrame) -> pd.DataFrame:
    filt = deptos["terrenoEdificado"].isna()
    deptos.loc[filt, "terrenoEdificado"] = deptos.loc[filt, "terrenoTotal"]
    filtro_P = deptos["precioUSD"].between(deptos["precioUSD"].quantile(0.005), deptos["precioUSD"].quantile(0.995))
    filtro_E = (deptos["terrenoEdificado"].between(10, 1500))
    return deptos.loc[filtro_P & filtro_E]
  
  def casas_filter(self, casas: pd.DataFrame) -> pd.DataFrame:
    filtro_P = casas["precioUSD"].between(casas["precioUSD"].quantile(0.005), casas["precioUSD"].quantile(0.995))
    filtro_E = casas['terrenoEdificado'].between(50, 2000)
    filtro_T = (casas['terrenoTotal'].between(casas['terrenoTotal'].quantile(0.01), 
                                              casas['terrenoTotal'].quantile(0.97))) | casas['terrenoTotal'].isna()
    return casas.loc[filtro_P & filtro_E & filtro_T]
  

class FilterML(StrategyFilter):
  def specific_gral_filter(self, df: pd.DataFrame) -> pd.DataFrame:
    filt = (df["tipoPropiedad"] == "CASA") | (df["tipoPropiedad"] == "DEPARTAMENTO") | (df["tipoPropiedad"] == "TERRENO")
    df = df.loc[filt]
    
    df = df.loc[~((df['terrenoEdificado'] == 1) | 
                  (df['terrenoEdificado'] == 1) |
                  (df['precioUSD'] == 1))]
    
    df.loc[~(df['ciudad'] == 'CAPITAL FEDERAL')]

    filt = df['barrio'].str.contains('INMUEBLES', na=False)
    df.loc[filt, 'barrio'] = np.nan

    departamentos = ['CALAMUCHITA', 'COLON', 'CRUZ DEL EJE',
                     'GENERAL ROCA', 'GENERAL SAN MARTIN', 'ISCHILIN', 'JUAREZ CELMAN',
                     'MARCOS JUAREZ', 'MINAS', 'POCHO', 'PUNILLA', 'RIO CUARTO', 'RIO PRIMERO',
                     'RIO SECO', 'RIO SEGUNDO', 'SAN ALBERTO', 'SAN JAVIER', 'SAN JUSTO',
                     'SANTA MARIA', 'TERCERO ARRIBA', 'TOTORAL', 'TULUMBA', 'UNION']
    filt = df['ciudad'].isin(departamentos)
    df.loc[filt, 'ciudad'] = df.loc[filt, 'barrio']
    filt = (df['ciudad'] == df['barrio'])
    df.loc[filt, 'barrio'] = np.nan
    return df
  
  def terrenos_filter(self, terrenos: pd.DataFrame) -> pd.DataFrame: 
    filtro_P = terrenos["precioUSD"].between(1500, terrenos['precioUSD'].quantile(0.995))
    filtro_T = (terrenos['terrenoTotal'].between(10,
                                                 terrenos['terrenoTotal'].quantile(0.995)))
    return terrenos.loc[filtro_P & filtro_T]
  
  def deptos_filter(self, deptos: pd.DataFrame) -> pd.DataFrame: 
    filt1 = (deptos['terrenoEdificado'] < 15) | (deptos['terrenoEdificado'].isna())
    filt2 = deptos['terrenoTotal'].notna()
    deptos.loc[filt1 & filt2, 'terrenoEdificado'] = deptos.loc[filt1 & filt2, 'terrenoTotal']
    filtro_P = deptos["precioUSD"].between(deptos["precioUSD"].quantile(0.005),
                                           deptos["precioUSD"].quantile(0.995))
    filtro_E = (deptos["terrenoEdificado"].between(10, 1500))
    return deptos.loc[filtro_P & filtro_E]
  
  def casas_filter(self, casas: pd.DataFrame) -> pd.DataFrame: 
    filtro_P = casas["precioUSD"].between(casas["precioUSD"].quantile(0.005),
                                          casas["precioUSD"].quantile(0.995))
    filtro_E = casas['terrenoEdificado'].between(15, 2500)
    filtro_T = (casas['terrenoTotal'].between(casas['terrenoTotal'].quantile(0.001),
                                              casas['terrenoTotal'].quantile(0.95))) | casas['terrenoTotal'].isna()
    return casas.loc[filtro_P & filtro_E & filtro_T]
  
  
class FilterZP(StrategyFilter):
  def specific_gral_filter(self, df: pd.DataFrame) -> pd.DataFrame:
    reemplazos = {
        "PH" : "DEPARTAMENTO",
        "TERRENOS" : "TERRENO"
    }
    df["tipoPropiedad"].replace(reemplazos, inplace= True)

    df = df.loc[~((df['terrenoEdificado'] == 1) | 
                  (df['terrenoEdificado'] == 1) |
                  (df['precioUSD'] == 1))]
    return df

  def terrenos_filter(self, terrenos: pd.DataFrame) -> pd.DataFrame: 
    filtro_P = terrenos["precioUSD"].between(
        1500, terrenos["precioUSD"].quantile(0.995))
    filtro_T = (terrenos['terrenoTotal'].between(10,
                                                 terrenos['terrenoTotal'].quantile(0.995)))
    terrenos = terrenos.loc[filtro_P & filtro_T]
  
  def deptos_filter(self, deptos: pd.DataFrame) -> pd.DataFrame: 
    filt1 = (deptos['terrenoEdificado'] < 15) | (deptos['terrenoEdificado'].isna())
    filt2 = deptos['terrenoTotal'].notna()
    deptos.loc[filt1 & filt2, 'terrenoEdificado'] = deptos.loc[filt1 & filt2, 'terrenoTotal']
    filtro_P = deptos["precioUSD"].between(deptos["precioUSD"].quantile(0.005),
                                           deptos["precioUSD"].quantile(0.995))
    filtro_E = (deptos["terrenoEdificado"].between(15, 500))
    return deptos.loc[filtro_P & filtro_E]
  
  def casas_filter(self, casas: pd.DataFrame) -> pd.DataFrame: 
    filt1 = (casas['terrenoTotal'] < casas['terrenoEdificado'])
    casas.loc[filt1, ['terrenoTotal', 'terrenoEdificado']] = casas.loc[filt1, ['terrenoEdificado', 'terrenoTotal']]
    filtro_P = casas["precioUSD"].between(casas["precioUSD"].quantile(0.005),
                                          casas["precioUSD"].quantile(0.995))
    filtro_E = casas['terrenoEdificado'].between(25, 2000)
    filtro_T = (casas['terrenoTotal'].between(casas['terrenoTotal'].quantile(0.001),
                                              casas['terrenoTotal'].quantile(0.999))) | casas['terrenoTotal'].isna()
    return casas.loc[filtro_P & filtro_E & filtro_T]