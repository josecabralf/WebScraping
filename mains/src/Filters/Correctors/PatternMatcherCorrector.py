import re
import pandas as pd

class PatternMatcherCorrector:
  def execute(self, df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df['barrio'].isna(), 'barrio'] = 'SD'
    df.loc[:, "barrio"] = df["barrio"].apply(self.patron_nueva_cba)
    df.loc[:, "barrio"] = df["barrio"].apply(self.patron_alta_cba)
    df.loc[:, "barrio"] = df["barrio"].apply(self.patron_manantiales)
    df.loc[:, "barrio"] = df["barrio"].apply(self.patron_docta)
    df.loc[:, "barrio"] = df["barrio"].apply(self.patron_centro)
    df.loc[:, "barrio"] = df["barrio"].apply(self.patron_gral)
    df.loc[:, "barrio"] = df["barrio"].apply(self.eliminar_simbolos)
    return df
  
  def patron_manantiales(self, nombre):
      if re.search(r'MANANTIALES', nombre):
          if re.search(r'DE MANANTIALES', nombre):
              patron = r'(\w+)\s+DE MANANTIALES'
              match = re.search(patron, nombre)
              if match: return match.group(1) + " DE MANANTIALES"
          return "MANANTIALES"
      return nombre

  def patron_nueva_cba(self, nombre):
      patron = r'.*(NUEVA CORDOBA|NVA CBA).*'
      if re.match(patron, nombre): return 'NUEVA CORDOBA'
      return nombre

  def patron_alta_cba(self, nombre):
      patron = r'.*(ALTA CORDOBA|ALTA CBA).*'
      if re.match(patron, nombre): return 'ALTA CORDOBA'
      return nombre
      
  def patron_docta(self, nombre):
      patron = r'.*DOCTA.*'
      if re.match(patron, nombre): return 'DOCTA'
      return nombre

  def patron_centro(self, nombre):
      patron = r'.*CENTRO.*'
      match = re.search(patron, nombre)
      if match:
          siguiente_palabra = re.search(r'CENTRO\s+(AMERICA)', nombre)
          if siguiente_palabra: return 'CENTRO AMERICA'
          return 'CENTRO'
      return nombre

  def patron_gral(self, nombre):
      if re.search(r'GRAL(\.)?', nombre):
          patron = r'GRAL\.?'
          nombre_transformado = re.sub(patron, 'GENERAL', nombre)
          return nombre_transformado
      return nombre

  def eliminar_simbolos(self, nombre):
      patron = r'[!¡."\'#$%&()*+,-/:;<=>?@[\]^_`{|}~]'
      nombre_limpio = re.sub(patron, '', nombre)
      nombre_limpio = nombre_limpio.replace('.', '')
      return nombre_limpio

